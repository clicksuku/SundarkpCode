#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fastembed import TextEmbedding
from sentence_transformers import SentenceTransformer
import numpy as np
from qdrant_client import QdrantClient, models
import csv
import json
import numpy as np
import enum
import pandas as pd


# In[2]:


def load_ground_truth():
    records=[]
    with open('ground-truth-data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            records.append(row)
        return records

def load_documents():
    documents = []
    with open('documents-with-ids.json', 'rb') as f_in:
        documents = json.load(f_in)
    return documents

def filter_ground_truth(filter:str):
    records = load_ground_truth()
    df_ground_truth = pd.DataFrame(records)    
    df_ground_truth = df_ground_truth[df_ground_truth[1] == filter]
    ground_truth = df_ground_truth.to_dict(orient='records')
    return ground_truth


# In[3]:


def hit_rate(relevance_total):
    cnt = 0

    for line in relevance_total:
        if True in line:
            cnt = cnt + 1

    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0

    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)

    return total_score / len(relevance_total)


# In[4]:


model_name = "jinaai/jina-embeddings-v2-small-en"
EMBEDDING_DIMENSIONALITY = 512


# In[5]:


client=None


# In[12]:


def setup_minsearch_qdrant(distance):
    global client
    client = QdrantClient("http://localhost:6333/")

    model = TextEmbedding(model_name=model_name)
    # Define the collection name
    collection_name = "zoomcamp-rag"

    # Create the collection with specified vector parameters
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIMENSIONALITY,  # Dimensionality of the vectors
            distance=distance  # Distance metric for similarity search
        )
    )

    documents=load_documents()
    points = []
    id = 0

    for doc in documents[:100]:
        question = doc['question']
        text = doc['text']
        course=doc['course']
        section=doc['section']
        doc_id=doc['id']
        qnText = doc['question'] + ' ' + doc['text']
        point = models.PointStruct(
            id=id,
            vector=models.Document(text=qnText, model=model_name), #embed text locally with "jinaai/jina-embeddings-v2-small-en" from FastEmbed
            payload={
                "question": question,
                "text": text,
                "section": section,
                "course": course,
                "doc_id":doc_id
            } #save all needed metadata fields
        )
        points.append(point)
        id += 1

        client.upsert(
            collection_name=collection_name,
            points=points
        )


# In[13]:


distance=models.Distance.COSINE
setup_minsearch_qdrant(distance)


# In[14]:


def minsearch_vector_search_qdrant(question,course):
    collection_name = "zoomcamp-rag"
    results = client.query_points(
        collection_name=collection_name,
        query=models.Document( #embed the query text locally with "jinaai/jina-embeddings-v2-small-en"
            text=question,
            model=model_name 
        ),
        limit=5, # top closest matches
        with_payload=True #to get metadata in the results
    )
    return results


# In[15]:


def compute_relevance(record, result):
    doc_id=record[2]
    doc_ids = [point.payload['doc_id'] for point in result.points]
    print(doc_id)
    print(doc_ids)
    relevance=[id==doc_id for id in doc_ids]
    print(relevance)
    return relevance

## Computing relevances

# Computing results
def compute_results(ground_truth):
    results=[]
    relevances=[]

    for record in ground_truth[:75]:
        question=record[0]
        course=record[1]
        result=minsearch_vector_search_qdrant(question,course)
        relevance=compute_relevance(record,result)
        results.append(result)
        relevances.append(relevance)
    return results,relevances


# In[16]:


filter:str='machine-learning-zoomcamp'
ground_truth=filter_ground_truth(filter)
results, relevances = compute_results(ground_truth)
print("hit_rate:" + str(hit_rate(relevances)))
print("mrr:" + str(mrr(relevances)))    


# In[29]:


from sentence_transformers import SentenceTransformer

model_name = 'multi-qa-MiniLM-L6-cos-v1'
model = SentenceTransformer(model_name)


# In[19]:


def cosine(u, v):
    u_norm = np.sqrt(u.dot(u))
    v_norm = np.sqrt(v.dot(v))
    return u.dot(v) / (u_norm * v_norm)


# In[36]:


def load_cosine_results():
    cosine_results=[]
    with open('results-gpt4o-mini.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            cosine_results.append(row)
        return cosine_results

df_results=pd.DataFrame()

def return_cosine_results_df():
    global df_results
    records = load_cosine_results()
    df_results = pd.DataFrame(records)    
    rag_real_results = df_results.to_dict(orient='records')
    return rag_real_results


# In[37]:


rag_real_results=return_cosine_results_df()


# In[30]:


def compute_similarity(record):
    answer_orig = record[2]
    answer_llm = record[1]

    v_llm = model.encode(answer_llm)
    v_orig = model.encode(answer_orig)

    return cosine(v_orig,v_llm)


# In[32]:


similarity = []

for record in rag_real_results:
    sim = compute_similarity(record)
    print(sim)
    similarity.append(sim)



# In[38]:


df_results['cosine'] = similarity
df_results['cosine'].describe()


# In[ ]:




