from openai import OpenAI
from dotenv import load_dotenv
from storage import save_tasks, load_tasks
from task import Task
import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

conversation_history = []

def chat(user_message):
    conversation_history.append({
        "role":"user",
        "content": user_message
    })

    tasks = load_tasks()
    task_list =  "\n".join([f"- [{t.status}] {t.title} (Priority: {t.priority}, Due: {t.due_date})" for t in tasks]) or "No tasks yet"

    system_prompt = f"""
    You are a helpful personal task management assistant
    
    Current Task:
    {task_list}
    
    You can help the user:
    - Add a task
    - List their tasks
    - Mark tasks as done
    - Delete tasks
    - Suggest priorities
    - Give daily briefings
    
    When the user wants to add a task, extract:
    - title
    - description
    - due_date (YYYY-MM-DD format)
    - priority (low/medium/high)

    Respond in this JSON format when adding a task:
    {{"action": "add_task", "title": "...", "description": "...", "due_date": "...", "priority": "..."}}
    
    For listing tasks respond:
    {{"action": "list_tasks"}}
    
    For marking done respond:
    {{"action": "mark_done", "index": <number starting from 0>}}
    
    For delete respond:
    {{"action": "delete_task", "index": <number starting from 0>}}
    
    For general conversation respond:
    {{"action": "chat", "message": "your respond here"}}
    
    Always respond with valid JSON only, nothing else
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *conversation_history
        ]
    )

    reply = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return handle_action(reply, tasks)

def handle_action(reply, tasks):
    try:
        reply = reply.strip()
        if reply.startswith("'''"):
            reply = reply.split("'''")[1]
            if reply.startswith("json"):
                reply = reply[4:]

        data = json.loads(reply)
        action = data.get("action")

        if action == "add_task":
            task = Task(
                data.get("title", "Untitled"),
                data.get("description", ""),
                data.get("due_date", ""),
                data.get("priority", "medium"),
            )
            tasks.append(task)
            save_tasks(tasks)
            return f"=== Task Added: {task.title} ===\n"

        elif action == "list_tasks":
            if not tasks:
                return "- No tasks yet -"
            result = "Your tasks:\n"
            for i, t in enumerate(tasks):
                result += f"{i+1}. [{t.status.upper()}] {t.title} (Priority: {t.priority}, Due: {t.due_date})\n"
                return result

        elif action == "mark_done":
            index = data.get("index", 0)
            if 0 <= index < len(tasks):
                task = tasks[index].mark_done()
                save_tasks(tasks)
                return f" Marked as done: {task[index].title}"
            return "- Task not found -"

        elif action == "delete_task":
            index = data.get("index", 0)
            if 0<= index < len(tasks):
                title = tasks[index].title
                tasks.pop(index)
                save_tasks(tasks)
                return f"=== Deleted: {title} ===\n"
            return "- Task not found -"

        elif action == "chat":
            return data.get("message", "How can I assist you?")

    except json.JSONDecodeError:
        return reply

