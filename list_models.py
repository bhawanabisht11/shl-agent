import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
}

response = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers=headers
)

print(response.json())