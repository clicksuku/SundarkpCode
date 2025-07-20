from fastmcp import FastMCP
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path("./.env")
load_dotenv(dotenv_path)

mcp = FastMCP("quotes_gen")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@mcp.tool
def generate_random_quote():
    """
        "type": "function",
        "name": "generate_random_quote",
        "description": "Generate a popular quote from the internet.",
        "parameters": {
            },
            "additionalProperties": False """
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {
            "role": "user",
            "content": "You are an amazing quote generator. So generate a popular quote. Please take care to not repeat the quotes"
            }
        ]
    )
    result =completion.choices[0].message.content
    print(result)
    return result;

@mcp.tool
def generate_quote(Author: str):
    """
        "type": "function",
        "name": "generate_quote",
        "description": "Generate quotes of the author passed to the tool. Please return only the quotes",
        "parameters": {
            "type": "object",
            "properties": {
                "Author": {
                    "type": "string",
                    "description": "The author from whom the quote is to be generated"
                }
            },
            "required": ["Author"],
            "additionalProperties": False """
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {
            "role": "user",
            "content": "Get the top quote of " + Author + "."
            }
        ]
    )
    result =completion.choices[0].message.content
    print(result)
    return result;


@mcp.resource("resource://sources")
def quotes_library() -> list[str]:
    return [
        "The only way to do great work is to love what you do.",
        "The best way to predict the future is to invent it.",
        "The only way to do great work is to love what you do.",
        "The best way to predict the future is to invent it.",
        "The only way to do great work is to love what you do.",
        "The best way to predict the future is to invent it.",
    ]

if(__name__ == "__main__"):
    mcp.run()
