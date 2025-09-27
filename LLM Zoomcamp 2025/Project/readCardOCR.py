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

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def loadCardDetailsJson(schema_file:str) -> dict:
    with open(schema_file, "r") as f:
        return json.load(f)


def loadCardDetailsImage(image_path:str):
    card_schema = loadCardDetailsJson("cardDetails.schema.json")

    client = OpenAI(
    api_key=OPENAI_API_KEY,  # this is also the default, it can be omitted
    base_url=OPENAI_BASE_URL
    )

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
            print("Card is valid and active")
            return True
        else:
            print("Card is invalid or expired")
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
    return results
    
async def main(type:str, details:str,rag:ragSolution):
    if type == "image":
        cardDetails = loadCardDetailsImage(details)
    elif type == "json":
        card = loadCardDetailsJson(details)
        cardDetails = json.dumps(card)
    elif type == "csv":
        cardDetails = details
    
    print(cardDetails)
    validity= await validateCardDetails(cardDetails)
    errorDescription = await checkRiskComplianceForCard(cardDetails)
    print("validity: ", validity)
    print("Risk and Compliance Status: ", errorDescription)
    code = errorDescription.split(":")[0]
    description=errorDescription.split(":")[1]
    print("Error Code: ", code)
    print("Error Description: ", description)
    results = await search(errorDescription, rag)
    print(results)

async def setupRag():
    rag = ragSolution()
    await rag.prepare_data()
    return rag

"""if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, required=True)
    parser.add_argument("--cardDetails", type=str, required=True)
    args = parser.parse_args()

    type = args.type
    details = args.cardDetails
    rag = asyncio.run(setupRag())
    asyncio.run(main(type, details, rag))"""


if __name__== "__main__":
    rag = asyncio.run(setupRag())

    with open("./_transactions/Transactions data.csv", "r") as f:
        reader = csv.DictReader(f)
        type="csv"
        for row in reader:
            cardDetails = json.dumps(row)
            print(cardDetails)
            asyncio.run(main(type, cardDetails, rag))

