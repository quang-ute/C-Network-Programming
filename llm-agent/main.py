import os
from smolagents import ToolCallingAgent, LiteLLMModel, GradioUI, Tool

import sqlite3
from dotenv import load_dotenv

load_dotenv()
apikey=os.getenv("DEEPSEEK_API_KEY") 

llm_model = LiteLLMModel(
    model_id="deepseek/deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant capable of generating sql statement from text"
        }
    ]
)
class SQLExecutorTool(Tool):
    """
    A tool that executes SQL queries on the 'demo_db.sqlite' database.

    Args:
        query (str): A SQL query to execute.

    Returns:
        string: Query results as a string.
    """
    name = "sql_executor"
    description = (
        "Executes SQL queries on the SQLite database 'demo_db.sqlite'. "
        "Returns query results as a string."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "A valid SQL query string."
        }
    }
    output_type = "string"
    def forward(self,query: str) -> str:
        db_file = "demo_db.sqlite"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            conn.commit()
        except Exception as e:
            results = f"SQL Execution Error: {e}"
        finally:
            conn.close()
        return str(results)
    
def get_db_schema(db_path: str) -> str:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(employees)")
        columns = cursor.fetchall()
        conn.close()

        schema_lines = [f" - {col[1]} ({col[2]})" for col in columns]
        return "\n".join(schema_lines)


sql_tool = SQLExecutorTool()

schema_description = get_db_schema('demo_db.sqlite')

agent = ToolCallingAgent(
    tools=[sql_tool],
    model=llm_model,
    description=f"{schema_description}\nUse the sql_executor tool to run SQL queries."
)
print(schema_description)

# prompt = "Find the name and salary of the employee with the highest salary. "
# result = agent.run(prompt)
# print(result)

GradioUI(agent).launch()