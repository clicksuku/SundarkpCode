#!/usr/bin/env python
# coding: utf-8

# In[38]:


import os
import json
from dotenv import load_dotenv

import pandas as pd
import tqdm

from openai import OpenAI


# In[2]:


load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL")


# In[6]:


documents_url="cards_decline_codes.json"


# In[18]:


import hashlib

def generate_document_id(doc):
    # combined = f"{doc['course']}-{doc['question']}"
    combined = f"{doc['code']}-{doc['Reason'][:10]}-{doc['Description'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id


# In[64]:


documents = []


# In[65]:


with open(documents_url, 'r') as f:
        documents = json.load(f)


# In[66]:


for doc in documents:
    doc['id']=generate_document_id(doc)


# In[68]:


with open(documents_url, 'w') as f_out:
    json.dump(documents, f_out, indent=2)


# In[32]:


prompt_template = """
You emulate a Payments Simulator which understands Credit Card decline codes and errors. 
You understand the decline codes and special decline conditions and limits and fault errors from the 
popular schemes such as VISA, Mastercard, Amex, Discover, JCB, UnionPay, Maestro, Electron, etc.

Formulate 5 description for a given Decline Code and Reason. 
The record should contain a clear description of the decline code and reason.
All the descriptions should be clear and concise.
All the 5 descriptions should be distinct. 

The record:

Decline Code: {code}
Reason: {Reason}
Description: {Description}

Provide the output in parsable JSON without using code blocks:

["Description1", "Description2", ..., "Description5"]
""".strip()


# In[33]:


def generate_questions(doc):
    prompt = prompt_template.format(**doc)

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}]
    )

    json_response = response.choices[0].message.content
    return json_response


# In[34]:


from tqdm.auto import tqdm


# In[35]:


documents[0]


# In[39]:


client = OpenAI(
    api_key=OPENAI_API_KEY,  # this is also the default, it can be omitted
    base_url=OPENAI_BASE_URL
    )


# In[41]:


for doc in tqdm.tqdm(documents): 
    doc_id = doc['id']
    if doc_id in results:
        continue

    questions = generate_questions(doc)
    results[doc_id] = questions


# In[44]:


results


# In[48]:


parsed_results = {}

for doc_id, json_questions in results.items():
    parsed_results[doc_id] = json.loads(json_questions)


# In[49]:


doc_index = {d['id']: d for d in documents}


# In[52]:


final_results = []

for doc_id, descriptions in parsed_resulst.items():
    code = doc_index[doc_id]['code']
    reason = doc_index[doc_id]['Reason']
    for desc in descriptions:
        final_results.append((code, reason, desc, doc_id))


# In[57]:


df = pd.DataFrame(final_results, columns=['code', 'Reason', 'Description', 'doc_id'])


# In[58]:


df.to_csv('ground-truth-data.csv', index=False)


# In[69]:


import json

with open(documents_url, 'rt') as f_in:
    documents = json.load(f_in)


# In[70]:


documents[0]


# In[95]:


from qdrant_client import QdrantClient, models
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# In[96]:


model_handle = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSIONALITY = 384
client = QdrantClient("http://localhost:6333/")
collection_name = "payments-eval-rag"


# In[119]:


def process_documents():
    loader = PyPDFDirectoryLoader("../_pdfs")
    docs = loader.load()
    txt_splitters = RecursiveCharacterTextSplitter(
            chunk_size=200, 
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "?", "!", " ", ""],
        )

    return txt_splitters.split_documents(docs)


# In[120]:


def check_collection_exists():
    return client.collection_exists(collection_name=collection_name)


# In[121]:


def insert_into_qdrant(data:list[str]):
    points = []
    id = 0

    for datum in data:
        point = models.PointStruct(
            id=id,
            vector=models.Document(text=datum, model=model_handle),
            payload={
                "text": datum,
            } #save all needed metadata fields
        )
        points.append(point)
        id += 1

    print(points[0])
    # Create the collection with specified vector parameters
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIMENSIONALITY,  # Dimensionality of the vectors
            distance=models.Distance.COSINE  # Distance metric for similarity search
        )
    )

    client.upsert(
        collection_name=collection_name,
        points=points,
    )


# In[122]:


def prepare_data():
    if check_collection_exists():
        print("Collection exists")
        return
    chunks = process_documents() #Created document chunks
    chunk_texts =  list(map(lambda d:d.page_content, chunks))
    insert_into_qdrant(chunk_texts)


# In[123]:


prepare_data()


# In[ ]:




