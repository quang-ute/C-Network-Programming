from dotenv import load_dotenv
from litellm import completion
import os
from rich import print

load_dotenv()

api_key = os.environ["GROQ_API_KEY"]

def get_llm_response(message):
    response = completion(
        model="groq/deepseek-r1-distill-llama-70b",
        api_key = api_key,
        messages=message,
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False
    )
    return response

messages = [
    {
        "role":"system",
        "content":"You are a helpful AI assistant"
    },
    {
        "role":"user",
        "content":"Who are you?"
    }
]


response = get_llm_response(messages)
print(response)