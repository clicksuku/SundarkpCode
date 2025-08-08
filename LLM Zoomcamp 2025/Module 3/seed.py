import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
from eval import *
import csv
import json
import numpy as np
from minsearch import VectorSearch, Index
import os

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

""" def return_doc_idx(documents):
    doc_idx = {d['id']: d for d in documents}
    return doc_idx
 """
def return_ground_truth():
    records = load_ground_truth()
    df_ground_truth = pd.DataFrame(records)    
    df_ground_truth = df_ground_truth[df_ground_truth[1] == 'machine-learning-zoomcamp']
    ground_truth = df_ground_truth.to_dict(orient='records')
    return ground_truth


def return_embeddings(model, documents):
    vectors = []    
    for doc in documents:
        question = doc['question']
        text = doc['text']
        vector = model.encode(question + ' ' + text)
        vectors.append(vector)
    return vectors

vindex=None
index=None

def setup_minsearch(is_vector_search:bool):
    global vindex
    global index
    documents=load_documents()
    
    if(not is_vector_search):
        index=Index(text_fields=["question", "section", "text"],
                keyword_fields=["course", "id"])
        index.fit(documents)
    else:
        model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
        vectors = []

        for doc in documents:
            question = doc['question']
            text = doc['text']
            vector = model.encode(question + ' ' + text)
            vectors.append(vector)
        
        vectors = np.array(vectors)
        vindex=VectorSearch(keyword_fields=["course", "id"]) 
        vindex.fit(vectors,documents) 

    
def minsearch_text_search(question,course):
    boost = {'question': 1.5, 'section': 0.1}
    #print(question)
    return index.search(
        question,
        filter_dict={'course': course},
        #boost_dict=boost,
        num_results=5
    )

def minsearch_vector_search(question, course):
    boost = {'question': 1.5, 'section': 0.1}
    model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
    v_question = model.encode(question)
    
    return vindex.search(
        v_question,
        filter_dict={'course': course},
        boost_dict=boost,
        num_results=5
    )

def minsearch_search(question,course,vector_Search):
    if(vector_Search):
        response=minsearch_vector_search(question,course)
        return response
    else:
        response=minsearch_text_search(question,course)
        return response

def compute_relevance(record, result):
    doc_id=record[2]
    relevance=[d['id']==doc_id for d in result]
    #print(relevance)
    return relevance
    

def compute_relevances_forAllQuestions(ground_truth):
    results=[]
    relevances=[]
    for record in ground_truth:
        question=record[0]
        course=record[1]
        result=minsearch_search(question,course,vector_Search)
        relevance=compute_relevance(record,result)
        results.append(result)
        relevances.append(relevance)
    return relevances

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

if(__name__ == "__main__"):
    vector_Search=True
    setup_minsearch(vector_Search)
    ground_truth=return_ground_truth()
    relevances = compute_relevances_forAllQuestions(ground_truth)
    print("hit_rate:" + str(hit_rate(relevances)))
    print("mrr:" + str(mrr(relevances)))
    
    
    
