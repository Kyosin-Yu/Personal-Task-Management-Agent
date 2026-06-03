from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

models = client.models.list()
free_models = [m.id for m in models.data if "free" in m.id]
for m in free_models:
    print(m)