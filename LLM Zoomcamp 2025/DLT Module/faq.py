import requests
import dlt
from dlt.destinations import qdrant

qdrant_destination = qdrant(
  qd_path="db.qdrant", 
)

@dlt.resource(name='course_data', table_name='course_data')
def get_course_data():
    docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    for course in documents_raw:
        course_name = course['course']

        for doc in course['documents']:
            doc['course'] = course_name
            yield doc


if __name__ == '__main__':
    #for doc in zoomcamp_data():
        #print(doc)

    #get_course_data()

    pipeline = dlt.pipeline(
        pipeline_name="zoomcamp_pipeline",
        destination=qdrant_destination,
        dataset_name="course_data"
    )
    load_info = pipeline.run(get_course_data())
    print(pipeline.last_trace)