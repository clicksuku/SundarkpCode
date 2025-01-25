from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


""" def create_embeddings(chunks:list[Document]):
    model_name = "BAAI/bge-large-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
    huggingFaceEmbedding = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )  
    embeddings = huggingFaceEmbedding.embed_documents(chunks)
    return embeddings

def create_embeddings_for_query(query)->list[float]:
    model_name = "BAAI/bge-large-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
    huggingFaceEmbedding = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
    query_embeddings = huggingFaceEmbedding.embed_query(query)
    return query_embeddings """

async def vectorize(chunks:List[Document]):
    chunk_texts =  list(map(lambda d:d.page_content, chunks))

    for chunk in chunk_texts:
        print(chunk)

    metadatas = [{"source": f"{i}-pl"} for i in range(len(chunks))]

    embeddings = OpenAIEmbeddings()
    docSearch = Chroma.from_texts(chunk_texts, embeddings, metadatas=metadatas)
    return docSearch
