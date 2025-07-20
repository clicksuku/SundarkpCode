import asyncio
from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("quotes_gen_mcp_server.py") as client:
        tools = await client.list_tools()
        print("Generated Tools:")
        for tool in tools:
            print(f"- {tool.name}")
    
        result = await client.call_tool("generate_quote", {"Author": "Albert Einstein"})
        result2 = await client.call_tool("generate_random_quote")
        print(f"Result: {result.content[0].text}")
        print(f"Result: {result2.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())