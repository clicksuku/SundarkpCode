from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
import bs4
from utils.enumUrls import enumerate_urls

resPages = []

async def process_url(urlPath:str):
    pages = []
    links  = enumerate_urls(urlPath)
    loader = WebBaseLoader(links,verify_ssl=False)

    async for doc in loader.alazy_load():
        doc.page_content = " ".join(doc.page_content.split())
        pages.append(doc)
    
    resPages.extend(pages)

async def process_document(docPath:str):
    loader = PyPDFLoader(docPath)
    docs = loader.load()
    resPages.extend(docs)
    return ""

async def load_process_docs(inputs:dict):
    urls = inputs["urls"]
    files = inputs["files"]
    
    for file in files:
        await process_document(file)

    for url in urls:
        await process_url(url)

    txt_splitters = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "?", "!", " ", ""],
        )
    chunks = txt_splitters.split_documents(resPages)
    return chunks