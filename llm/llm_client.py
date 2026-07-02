from openai import OpenAI
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
# just for check
#print("API Key:", os.getenv("GROQ_API_KEY"))

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
print(os.getenv("GROQ_API_KEY"))
'''
client = OpenAI(
    api_key="YOUR_GROQ_API_KEY",
    base_url="https://api.groq.com/openai/v1"
)
'''

def generate_response(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an SHL assessment assistant. You ONLY use provided context. Never invent assessments."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content