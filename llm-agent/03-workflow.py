from dotenv import load_dotenv
from langchain_litellm import ChatLiteLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool
import datetime
import os
from rich import print

load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

llm = ChatLiteLLM(
    model="gemini/gemma-3-27b-it",
)

# Define the Google Calendar tool
class GoogleCalendarTool(BaseTool):
    name: str = "Google Calendar"
    description: str = "Fetches information about your upcoming meetings and events from Google Calendar. Use this tool to check your schedule."
    
    def _run(self, query: str) -> str:

        now = datetime.datetime.now()       
        mock_meetings = [
            {
                "title": "Client Presentation",
                "time": "10:00 AM",
                "date": (now + datetime.timedelta(days=5)).strftime("%A, %B %d"),
                "attendees": "Client team, sales"
            }
        ]
        next_meeting = mock_meetings[0]
        return f"Your next meeting is '{next_meeting['title']}' at {next_meeting['time']} on {next_meeting['date']} with {next_meeting['attendees']}."



#Initialize the agent
agent = initialize_agent(
    tools=[GoogleCalendarTool()],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the agent with a sample query
print(agent.invoke("When is my next meeting?"))