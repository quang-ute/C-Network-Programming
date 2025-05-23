import os
from dotenv import load_dotenv
from rich import print 
from netutils import NetworkTools

from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    LiteLLMModel,
)

load_dotenv()
apikey=os.getenv("DEEPSEEK_API_KEY") 


llm_model = LiteLLMModel(
    model_id="deepseek/deepseek-chat",
    messages=[
        {"role": "system",
         "content": "You are a helpful AI assistant capable of using tools to perform tasks. "
         "When given a query, analyze it and use available tools to gather information. "
         "Return JSON responses when possible."
        }
    ]
)

nettools = [DuckDuckGoSearchTool(),NetworkTools.get_delay_time]    
agent = CodeAgent(tools=nettools, 
                  model=llm_model,
                  verbosity_level=2,
                  additional_authorized_imports=["matplotlib","matplotlib.pyplot","numpy","pandas","datetime"],
                )
query0 = """
Plot chart to visualize network packet travel time from this computer to google.com, amazon.com, and facebook.com by
sending at least 10 ICMP packets to each target, do NOT use a bar chart.
"""

query1 = """
How long would it take for a puma to cross the united states from florida to california?
"""
query2="""
What are favorite sports of Meta current CEO?
"""
query3="""
What are most run pentest apps and usage percentage of every app recently?"
"""

result = agent.run(query1)

print(result)   