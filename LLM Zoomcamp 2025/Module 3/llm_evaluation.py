#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import json
import os
from openai import OpenAI
from tqdm.auto import tqdm


# In[2]:


docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)


# In[4]:


docs_response


# In[5]:


documents_raw = docs_response.json()


# In[6]:


documents=[]
for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course']=course_name
        documents.append(doc)


# In[7]:


import hashlib

def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id


# In[8]:


for document in documents:
    document_id=generate_document_id(document)
    document['id']=document_id


# In[9]:


documents[0]


# In[10]:


from collections import defaultdict 


# In[11]:


hashes = defaultdict(list)
for document in documents:
    doc_id=document['id']
    hashes[doc_id].append(document)


# In[12]:


len(documents), len(hashes)


# In[13]:


for k, values in hashes.items():
    if len(values) < 1:
        print(k, len(values))


# In[14]:


with open('documents-with-ids.json', 'wt') as f_out:
    json.dump(documents, f_out, indent=2)


# In[22]:


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# In[28]:


def generate_questions(doc):
    prompt = prompt_template.format(**doc)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )

    json_response = response.choices[0].message.content
    return json_response


# In[29]:


prompt_template = """
You emulate a student who's taking our course.
Formulate 5 questions this student might ask based on a FAQ record. The record
should contain the answer to the questions, and the questions should be complete and not too short.
If possible, use as fewer words as possible from the record. from tqdm.auto import tqdm


The record:

section: {section}
question: {question}
answer: {text}

Provide the output in parsable JSON without using code blocks:

["question1", "question2", ..., "question5"]
""".strip()


# In[30]:


from tqdm.auto import tqdm


# In[31]:


results = {}


# In[33]:


for doc in tqdm(documents): 
    doc_id = doc['id']
    if doc_id in results:
        continue

    questions = generate_questions(doc)
    results[doc_id] = questions


# In[41]:


serialized_results = pickle.dumps(results)


# In[43]:


with open("results.bin", "wb") as f:
       f.write(serialized_results)


# In[44]:


import pickle


# In[45]:


with open('results.bin', 'rb') as f_in:
    results = pickle.load(f_in)


# In[46]:


results['1f6520ca']


# In[47]:


parsed_resulst = {}

for doc_id, json_questions in results.items():
    parsed_resulst[doc_id] = json.loads(json_questions)


# In[65]:


first_key = list(results.keys())[1]
print(first_key)


# In[109]:


clean_results['46acdd18']


# In[52]:


clean_results = {key.strip(): item.strip() for key, item in results.items()}


# In[101]:


clean_results={}

for key,value in results.items():
    newValue=value.replace('\n', '')
    newValue=newValue.replace('\\d', '')
    newValue=newValue.replace('\'', '')
    newValue=newValue.replace('//', '')
    newValue=newValue.replace('<', '')
    newValue=newValue.replace('>', '')
    newValue=newValue.replace(':', '')
    newValue=newValue.replace('  ', '')
    clean_results[key] = newValue.replace('    ', '')


# In[114]:


clean_results['46acdd18']='["What are the steps to set up a notebook in Google Colab for deep learning projects?","How do I select the GPU type when using Google Colab for my deep learning tasks?","Is it possible to import an existing notebook into Google Colab for neural network training?","Where can I find the option to change the runtime type in Google Colab?","What type of GPU should I choose for optimal performance in Google Colab?"]'


# In[115]:


parsed_resulst = {}

for doc_id, json_questions in clean_results.items():
    print(doc_id)
    parsed_resulst[doc_id] = json.loads(json_questions)


# In[116]:


doc_index = {d['id']: d for d in documents}


# In[117]:


doc_index


# In[118]:


final_results = []

for doc_id, questions in parsed_resulst.items():
    course = doc_index[doc_id]['course']
    for q in questions:
        final_results.append((q, course, doc_id))


# In[119]:


final_results[0]



# In[120]:


df = pd.DataFrame(final_results, columns=['question', 'course', 'document'])


# In[121]:


df.to_csv('ground-truth-data.csv', index=False)



documents = []

with open('documents-with-ids.json', 'rb') as f_in:
    documents = json.load(f_in)


# In[127]:


len(documents)


import csv

def load_csv():
    records=[]
    with open('ground-truth-data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            records.append(row)
        return records


# In[162]:


records = load_csv()
df_ground_truth = pd.DataFrame(records)    


# In[163]:


len(records)


# In[165]:


df_ground_truth = pd.DataFrame(records)


# In[176]:


print(df_ground_truth[1])


# In[172]:


df_ground_truth = df_ground_truth[df_ground_truth[1] == 'machine-learning-zoomcamp']


# In[180]:


len(df_ground_truth)


# In[181]:


ground_truth = df_ground_truth.to_dict(orient='records')


# In[ ]:





# In[184]:


doc_idx = {d['id']: d for d in documents}


# In[196]:


doc_idx['5170565b']['text']


# In[ ]:





# In[ ]:





# In[213]:


from sentence_transformers import SentenceTransformer
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


# In[ ]:


from tqdm.auto import tqdm

vectors = []
for doc in tqdm(documents):
    question = doc['question']
    text = doc['text']
    vector = model.encode(question + ' ' + text)
    vectors.append(vector)

