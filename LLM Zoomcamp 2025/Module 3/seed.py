import csv
import json
import numpy as np
import enum

import pandas as pd
from sentence_transformers import SentenceTransformer

from minsearch import VectorSearch, Index
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline

from fastembed import TextEmbedding
from sentence_transformers import SentenceTransformer
import numpy as np
from qdrant_client import QdrantClient, models

##Loading Documents required for Analysis

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

## End of Loading documents

#Calculating Hit rate and MRR

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


## End of Calculating Hit rate and MRR

class SearchModel(enum.StrEnum):
    TEXT = "Text",
    VSEARCH_ST = "Vector_Search_Sentence_Transform",
    VSEARCH_TSVD = "Vector_Search_Truncated_SVD",
    VSEARCH_QDRANT = "Vector_Search_Qdrant"

vindex=None
index=None
svdindex=None
pipeline=None
client=None
model_name = "jinaai/jina-embeddings-v2-small-en"
EMBEDDING_DIMENSIONALITY = 512


def setup_minsearch_text():
    global index
    documents=load_documents()
    
    index=Index(text_fields=["question", "section", "text"],
            keyword_fields=["course", "id"])
    index.fit(documents)
    
def setup_minsearch_Transform():
    global vindex
    documents=load_documents()

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

def setup_minsearch_SVD():
    global svdindex
    global pipeline
    documents=load_documents()
    texts=[]

    for doc in documents:
        question = doc['question']
        text = doc['text']
        t = doc['question'] + ' ' + doc['text']
        texts.append(t)
    
    pipeline = make_pipeline(
        TfidfVectorizer(min_df=3),
        TruncatedSVD(n_components=128, random_state=1)
    )
    X = pipeline.fit_transform(texts)
    svdindex=VectorSearch(keyword_fields={"course"}) 
    svdindex.fit(X,documents) 

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

    for doc in documents:
        question = doc['question']
        text = doc['text']
        course=doc['course']
        section=doc['section']
        point = models.PointStruct(
            id=id,
            vector=models.Document(text=doc['text'], model=model_name), #embed text locally with "jinaai/jina-embeddings-v2-small-en" from FastEmbed
            payload={
                "question": question,
                "text": text,
                "section": section,
                "course": course
            } #save all needed metadata fields
        )
        points.append(point)
        id += 1

        client.upsert(
            collection_name=collection_name,
            points=points
        )


def setup_search(searchModel:str):
    if(searchModel==SearchModel.TEXT):
        setup_minsearch_text()
    elif(searchModel== SearchModel.VSEARCH_ST):
        setup_minsearch_Transform()
    elif(searchModel== SearchModel.VSEARCH_TSVD):
        setup_minsearch_SVD()
    elif(searchModel== SearchModel.VSEARCH_QDRANT):
        distance=models.Distance.DOT
        setup_minsearch_qdrant(distance)


def minsearch_text_search(question,course):
    boost = {'question': 1.5, 'section': 0.1}
    return index.search(
        question,
        filter_dict={'course': course},
        boost_dict=boost,
        num_results=5
    )

def minsearch_vector_search(question, course):
    boost = {'question': 1.5, 'section': 0.1}
    model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
    v_question = model.encode(question)
    
    return vindex.search(
        v_question,
        filter_dict={'course': course},
        num_results=5
    )

def minsearch_vector_search_withSVD(question, course):
    global svdindex
    global pipeline

    results = svdindex.search(
        pipeline.transform([question])[0],
        num_results=5)
    return results

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

def search(searchModel:str,question,course):
    if(searchModel==SearchModel.TEXT):
        result=minsearch_text_search(question,course)
    elif(searchModel== SearchModel.VSEARCH_ST):
        result=minsearch_vector_search(question,course)
    elif(searchModel== SearchModel.VSEARCH_TSVD):
        result=minsearch_vector_search_withSVD(question,course)
    elif(searchModel==SearchModel.VSEARCH_QDRANT):
        result=minsearch_vector_search_qdrant(question,course)
    return result

#Computing Relevances

def compute_relevance(record, result):
    doc_id=record[2]
    relevance=[d['id']==doc_id for d in result]
    return relevance

## Computing relevances

# Computing results
def compute_results(ground_truth, searchModel):
    results=[]
    relevances=[]
    
    for record in ground_truth[:2]:
        question=record[0]
        course=record[1]
        result=search(searchModel,question,course)
        relevance=compute_relevance(record,result)
        results.append(result)
        relevances.append(relevance)
    return results,relevances


## Computing Results


if(__name__ == "__main__"):
    searchModel=SearchModel.VSEARCH_QDRANT

    filter:str='machine-learning-zoomcamp'
    ground_truth=filter_ground_truth(filter)
    setup_search(searchModel)
    results, relevances = compute_results(ground_truth, searchModel)
    #print(results)
    #print(relevances)
    
    print("hit_rate:" + str(hit_rate(relevances)))
    print("mrr:" + str(mrr(relevances)))
    
    
    
