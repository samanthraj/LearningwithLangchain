from langchain_groq import ChatGroq
import os
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file




model = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

client = MultiServerMCPClient(
    {
        "time": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "mcp-server-time",
                "--local-timezone=America/New_York"
            ]
        }
    }
)

async def main():
    tools = await client.get_tools()

    agent = create_agent(
        model=model,
        tools=tools
    )

    response = await agent.ainvoke(
        {"messages": "what time is it in IST right now?"}
    )

    print(response["messages"][-1].content)

asyncio.run(main())