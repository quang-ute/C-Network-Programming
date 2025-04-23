from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool
from litellm import completion
import os
from rich import print

load_dotenv()

# api_key = os.environ["DEEPSEEK_API_KEY"]

# llm = ChatLiteLLM(
#     model="deepseek/deepseek-chat",
#     api_key=api_key,
#     api_base="https://api.deepseek.com/v1",
#     temperature=0,
# )
api_key = os.environ["GEMINI_API_KEY"]

llm = ChatLiteLLM(
    model="gemini/gemma-3-27b-it",
)

# Tool 1: DuckDuckGo Search
search = DuckDuckGoSearchRun()

# Tool 2: Wikipedia
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Tool 3: Python REPL (for calculations)
python_repl = PythonREPLTool()

# Create instances of the tools
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for finding current information or answering questions about recent events"
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Useful for getting factual information about people, places, and historical events"
    ),
    Tool(
        name="Calculator",
        func=python_repl.run,
        description="Useful for performing mathematical calculations and data analysis"
    )

]


# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the agent with a sample query
response = agent.invoke("What's the current population of Vietnam? Calculate the ratio of population between India and vietnam?")
print(response['output'])