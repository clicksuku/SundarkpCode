import os

import chainlit as cl
from chainlit.input_widget import Switch

from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import (
    ConversationalRetrievalChain
)

from utils.load_data import load_process_docs
from utils.vectorize_data import vectorize

async def solicit_inputs():
    #inputs = dict()
    keys = ["urls","files"]
    filePaths = []
    urls = []

    res = await cl.AskActionMessage(
        content="Pick an Input!",
        actions=[
            cl.Action(name="url", payload={"value": "url"}, label="✅ URL"),
            cl.Action(name="file", payload={"value": "file"}, label="✅ File"),
            cl.Action(name="done", payload={"value": "done"}, label="❌ done"),
        ],
        ).send()
    
    while res:
        match res.get("payload").get("value"):
            case "url":
                urlVal = await cl.AskUserMessage(
                    content="Enter a Valid URL:\n", 
                    timeout=180).send()
                if urlVal:
                    url = urlVal['output']
                    urls.append(url)
                    await cl.Message(content="URL is :" + url).send()
                    await cl.Message(content="Urls is :" + ','.join(urls)).send()
            case "file":
                files = await cl.AskFileMessage(
                    content="Please upload a text or file to begin!",
                    accept=["text/plain", "application/pdf"],
                    max_size_mb=20,
                    timeout=180,
                ).send()

                file = files[0]
                filePaths.append(file.path)
                await cl.Message(content="File Name is :" + file.path).send()
                await cl.Message(content="File Name is :" + ','.join(filePaths)).send()
            case "done":
                vals = []
                
                vals.append(urls)
                vals.append(filePaths)
                inputs = dict(zip(keys,vals))
                return inputs
        
        res = await cl.AskActionMessage(
            content="Pick an Input!",
            timeout=180,
            actions=[
                cl.Action(name="url", payload={"value": "url"}, label="✅ URL"),
                cl.Action(name="file", payload={"value": "file"}, label="✅ File"),
                cl.Action(name="done", payload={"value": "done"}, label="❌ done"),
            ],
            ).send()
    

@cl.on_chat_start
async def on_chat_start():
    msg = cl.Message(content="Welcome to the Knowledge Base Q&A. You can enter a URL or a file to build your knowledge base against which questions can be posted\n\n")
    await msg.send()

    inputs = await solicit_inputs()
    msg = cl.Message(content=f"Processing ...")
    await msg.send()

    chunks = await load_process_docs(inputs)
    docSearch = await vectorize(chunks=chunks)

    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True),
        chain_type="stuff",
        retriever=docSearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Let the user know that the system is ready
    msg.content = f"Processing  done. You can now ask questions!"
    await msg.send()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]  

    text_elements = []  

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(
                    content=source_doc.page_content, name=source_name, display="side"
                )
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()