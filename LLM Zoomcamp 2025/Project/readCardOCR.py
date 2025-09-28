import os
import json 
import base64
import argparse
import csv  
import asyncio

from dotenv import load_dotenv
from openai import OpenAI

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from rag.ragSolution import ragSolution

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=OPENAI_API_KEY,  # this is also the default, it can be omitted
    base_url=OPENAI_BASE_URL
    )

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def loadCardDetailsJson(schema_file:str) -> dict:
    with open(schema_file, "r") as f:
        return json.load(f)


def loadCardDetailsImage(image_path:str):
    card_schema = loadCardDetailsJson("cardDetails.schema.json")
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the mini model
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": "Provide the JSON file that represents this document. Use this JSON schema " + json.dumps(card_schema)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + encode_image_to_base64(image_path)
                        }
                    }
                ],
            }
        ],
        max_tokens=200,
        response_format={"type": "json_object"}
    )

    # Print the response from the model
    cardDetails = response.choices[0].message.content
    return cardDetails


async def validateCardDetails(cardDetails:str):
    transport = StreamableHttpTransport(url="http://127.0.0.1:8000/mcp")
    client = Client(transport)
    card = json.loads(cardDetails)
    cardNumber = card.get("cardNumber")
    expiryDate = card.get("expiryDate")
    async with client:
        isValid = await client.call_tool("isValidCardNumber", {"cardNumber": cardNumber})
        isActive = await client.call_tool("isCardActive", {"expiryDate": expiryDate})
        valid=isValid.structured_content.get("result")
        active=isActive.structured_content.get("result")

        if valid and active:
            return True
        else:
            return False

async def checkRiskComplianceForCard(cardDetails:str):
    transport = StreamableHttpTransport(url="http://127.0.0.1:8000/mcp")
    client = Client(transport)

    card = json.loads(cardDetails)
    cardNumber = card.get("cardNumber")
    async with client:
        errorCode = await client.call_tool("checkCardErrorCode", {"cardNumber": cardNumber})
        return errorCode.structured_content.get("result")


async def search(error:str, rag:ragSolution):
    results = await rag.search(error)
    text = results.points[0].payload['text']
    return text

async def build_prompt(declineCode:str, reason:str, description:str, results:str):
    prompt_template = """
    You understand the decline codes and special decline conditions and limits and fault errors from the 
    popular schemes such as VISA, Mastercard, Amex, Discover, JCB, UnionPay, Maestro, Electron, etc.
    The answer should contain a clear description of the decline code and reason.
    Use only the facts from the CONTEXT to provide the answer.
    
    Decline Code: {code}
    Reason: {Reason}

    CONTEXT: 
    {context}
    """.strip()

    context = f"Description: {description}\nSearch Results: {results}"
    prompt = prompt_template.format(code=declineCode, Reason=reason, context=context).strip()
    return prompt


async def respond_with_llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

    
async def main(type:str, details:str,rag:ragSolution):
    if type == "image":
        cardDetails = loadCardDetailsImage(details)
    elif type == "json":
        card = loadCardDetailsJson(details)
        cardDetails = json.dumps(card)
    elif type == "csv":
        cardDetails = details
    
    validity= await validateCardDetails(cardDetails)
    errorDescription = await checkRiskComplianceForCard(cardDetails)
    code = errorDescription.split(":")[0]
    reason=errorDescription.split(":")[1]
    description=errorDescription.split(":")[2]
    results = await search(errorDescription, rag)
    
    print("Card Details: ", cardDetails)
    print("validity: ", validity)

    if validity:
        print("Card is Valid and Active")
    else:
        print("Card is Invalid or Expired")

    print("code: ", code,"\n" )
    print("reason: ", reason,"\n" )
    print("description: ", description,"\n\n" )
    print("Raw Results: ", results,"\n\n" )
    prompt =await build_prompt(code, reason, description, results)
    #print("Prompt :", prompt)

    llm_response = await respond_with_llm(prompt)
    print("LLM Response :", llm_response,"\n\n" )

async def setupRag():
    rag = ragSolution()
    await rag.prepare_data()
    return rag

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True)
    parser.add_argument("--cardDetails", type=str, required=True)
    args = parser.parse_args()

    type = args.type
    details = args.cardDetails
    rag = asyncio.run(setupRag())

    if type == "image":
        asyncio.run(main(type, details, rag))    
    elif type == "json":
        asyncio.run(main(type, details, rag))
    elif type == "csv":
        with open("./_transactions/Transactions data.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cardDetails = json.dumps(row)
                asyncio.run(main(type, cardDetails, rag))
                input("Press Enter to continue...") # This is to prevent the program from exiting
    