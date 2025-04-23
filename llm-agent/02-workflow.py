from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool

import os
from rich import print

load_dotenv()
api_key = os.environ["GEMINI_API_KEY"]

llm = ChatLiteLLM(
    model="gemini/gemini-2.5-flash-preview-04-17",
)
@tool
def dummy_tool(query: str) -> str:
    """A dummy tool that just echoes the input"""
    return f"I received: {query}"


#Initialize the agent
agent = initialize_agent(
    tools=[dummy_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the agent with a sample query
print(agent.invoke("When is my next meeting?"))