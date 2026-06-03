from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def parse_task_from_input(user_input):
    prompt = f"""
    Extract task details from this input: "{user_input}"

    Reply in this exact format, nothing else:
    Title: <task title>
    Description: <short description>
    Due date: <date in YYYY-MM-DD format, or 'not specified'>
    Priority: <low, medium, or high>
    """

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def suggest_priority(title, description):
    prompt = f"""
    Given this task:
    Title: {title}
    Description: {description}

    Suggest a priority level (low, medium, or high) and explain why in one sentence.
    """

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content