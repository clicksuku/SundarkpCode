import os

import chainlit as cl
from chainlit.input_widget import Switch

from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import (
    ConversationalRetrievalChain
)

from utils.load_data import load_documents
from utils.vectorize_data import vectorize
from utils.text_to_audio import convertToAudio

@cl.on_chat_start
async def on_chat_start():
    settings = await cl.ChatSettings(
        [
            Switch(
                id="Audio",
                label="Audio",
                initial=False
            )
        ]
    ).send()
    
    url = "https://sahamati.org.in/"
    chunks = await load_documents(url)
    docSearch = await vectorize(chunks=chunks)

    msg = cl.Message(content=f"Processing ...")
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
    await msg.update()

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
    
    """ await convertToAudio(answer)

    elements = [
        cl.Audio(name="Answer", path="./speech.mp3", display="inline"),
    ]
    await cl.Message(
        content="Here is an audio file",
        elements=elements,
    ).send() """