from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
import os
from rich import print


load_dotenv()

api_key = os.environ["DEEPSEEK_API_KEY"]
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatLiteLLM(
    #model="deepseek/deepseek-chat",
    model = "openai/gpt-4o-mini",
#    api_key=api_key,
    #api_base="https://api.deepseek.com/v1",
    temperature=0,
)
@tool
def dummy_network_tool(query: str) -> str:
    """A dummy network tool """
    return f"I received: {query}"
# Initialize the agent
agent = initialize_agent(
    tools=[dummy_network_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the agent with a sample query
query = """Plot chart to display network packet travel time from this computer to google.com, amazon.com 
            and facebook.com. Send at least 10 packets for each target. 
            Do NOT plot using average travel time, DO NOT use bar chart."""
response = agent.invoke(query)
print(response)