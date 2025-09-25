import hashlib
import os
from keras import export
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL")

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from qdrant_client import QdrantClient, models
from langchain_huggingface import HuggingFaceEmbeddings


model_handle = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSIONALITY = 384
client = QdrantClient("http://localhost:6333/")
collection_name = "payments-rag"

class ragSolution:
    async def insert_into_qdrant(self, data:list[str]):
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


    async def search(self, query, limit=1):
        results = client.query_points(
            collection_name=collection_name,
            query=models.Document( 
                text=query,
                model=model_handle 
            ),
            limit=limit, 
            with_payload=True 
        )

        return results

    #change it to read from URL into Stream and read from stream here
    async def process_documents(self):
        loader = PyPDFDirectoryLoader("./_pdfs/")
        docs = loader.load()
        txt_splitters = RecursiveCharacterTextSplitter(
                chunk_size=400, 
                chunk_overlap=40,
                separators=["\n\n", "\n", ".", "?", "!", " ", ""],
            )

        return txt_splitters.split_documents(docs)

    async def prepare_data(self):
        chunks = await self.process_documents() #Created document chunks
        chunk_texts =  list(map(lambda d:d.page_content, chunks))
        await self.insert_into_qdrant(chunk_texts)
