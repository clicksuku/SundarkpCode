With an increased interest in Gen AI, LLM and RAG, I implemented a RAG application enhanced by LLM, and it queries against my profile to generate answers. The application can be seen working at https://sundarkp.streamlit.com/ (A little slow as it is hosted on Streamlit Community Cloud)

**What the Application does?**

**Concept** 
Sharing only the gist as there are better and well written articles on the same concept

•	LLM framework provides support for Document Loading, Splitting, creating Embeddings. I used LangChain Community for the same. 
•	Vectorization is an important element in RAG and LLM. Based on the semantic and structural aspects of words and sentences, the text is transformed into a numerical representation and stored in a form of databased called Vector Database
o	For generating vectors, I use HuggingFaceBgeEmbedding trained on bge-large-en-v1.5 language model. 
o	Pinecone is the vector database and it requires API key. 
•	Streamlit is used for the visualization
•	As a first step, RAG generate responses based on the document. 
•	The responses from RAG are set as context, and the query is posted to OpenAI (LLM) which generates better readable answers. 

**Code**
[Github Link]()


**Tech Stack**

Vector Database – Pinecone
LLM – OpenAI
LLM/RAG Framework – langchain
Embedding Model – HuggingFaceEmbedding (BAAI/bge-large-en-v1.5)

PDF Parser – PyPDF
Language - Python
