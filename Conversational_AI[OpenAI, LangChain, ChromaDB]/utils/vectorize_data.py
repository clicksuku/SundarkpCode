from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

async def vectorize(chunks:List[Document]):
    chunk_texts =  list(map(lambda d:d.page_content, chunks))
    metadatas = [{"source": f"{i}-pl"} for i in range(len(chunks))]

    embeddings = OpenAIEmbeddings()
    docSearch = Chroma.from_texts(chunk_texts, embeddings, metadatas=metadatas)
    return docSearch
