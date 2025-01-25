from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4
from utils.enumUrls import enumerate_urls

async def process_documents(urlPath:str):
    links  = enumerate_urls(urlPath)
    loader = WebBaseLoader(links,verify_ssl=False)

    pages = []
    async for doc in loader.alazy_load():
        doc.page_content = " ".join(doc.page_content.split())
        pages.append(doc)

    txt_splitters = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "?", "!", " ", ""],
        )
    chunks = txt_splitters.split_documents(pages)
    print(chunks)     
    return chunks

async def load_documents(filePath:str):
    chunks = await process_documents(filePath) #Created document chunks
    return chunks