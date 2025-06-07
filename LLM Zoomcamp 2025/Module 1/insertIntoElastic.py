import requests 
from elasticsearch8 import Elasticsearch
import tiktoken

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

#print(documents[2])

es = Elasticsearch(
    hosts='https://localhost:9200',
    basic_auth=('elastic', '_wzWIGSQM9sxXIyp4UMg'), 
    ca_certs='./http_ca.crt'
)

counter =0
for doc in documents:
    es.index(index='documents1', id=counter, document=doc)
    counter += 1

#print(es.get(index='documents1', id=2))

query1 = {
        "query": {
             "multi_match": {
                "query": "How do execute a command on a Kubernetes pod?",
                "fields": ["question^4", "text"],
                "type": "best_fields"
            }
        }
    }
#response = es.search(index="documents1", body=query1)
#print(response)

query2 = {
    "query": {
        "bool": {
            "should": [
                {"match": {"question": "How do copy a file to a Docker container?"}}
            ],
            "filter": [
                {"match": {"course": "machine-learning-zoomcamp"}}
            ]
        }
    }
}
    

response = es.search(index="documents1", body=query2)
#print(response)

context_template = """
Q: {question}
A: {text}
""".strip()


def create_context(response):
    context = []
    for hit in response['hits']['hits']:
        context.append(context_template.format(question=hit['_source']['question'], text=hit['_source']['text']))
    return '\n'.join(context)

context = create_context(response)

prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

question = "How do copy a file to a Docker container?"

prompt = prompt_template.format(question=question, context=context)

print(prompt)
print(len(prompt))

encoding = tiktoken.encoding_for_model("gpt-4o")

print(len(encoding.encode(prompt)))