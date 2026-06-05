from openai import OpenAI
from dotenv import load_dotenv
from storage import save_tasks, load_tasks
from task import Task
from smartFeatures import get_daily_briefing, get_priority_summary
from calendarHelper import add_calendar_event, delete_calendar_event, get_upcoming_events
from datetime import datetime
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
    pending_tasks = [t for t in tasks if t.status != "done"]
    task_list = "\n".join([
        f"- [{t.status}] {t.title} (Pending: {t.priority}, Due: {t.due_date})"
        for t in pending_tasks
    ]) or "- No Pending Tasks -"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_prompt = f"""
    You are a helpful personal task management assistant.
    The current date and time is: {now} (Malaysia Time, UTC+8)
    
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
    
    For adding to calendar or when adding a task with a due date respond:
    {{"action": "add_task", "title": "...", "description": "...", "due_date": "...", "priority": "...", "sync_calendar": true}}
    
    For adding a task respond:
    {{"action": "add_task", "title": "...", description": "...", "due_date": "YYYY-MM-DD", "due_time": "HH:MM or null", "priority": "...", "sync_calendar": true}}
    
    For checking calendar or upcoming events respond:
    {{"action": "check_calendar"}}
    
    For general conversation respond:
    {{"action": "chat", "message": "your respond here"}}
    
    For daily briefing or "what should I focus on" respond:
    {{"action": "daily_briefing"}}
    
    For priority ranking or scoring respond:
    {{"action": "priority_summary"}}
    
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

            result = f"=== Task Added: {task.title} ===\n"

            if data.get("sync_calendar") and task.due_date:
                calendar_result = add_calendar_event(
                    task.title,
                    task.description,
                    task.due_date,
                    data.get("due_time")
                )
                result += f"\n{calendar_result}"
            return result

        elif action == "check_calendar":
            return get_upcoming_events()

        elif action == "list_tasks":
            pending  = [t for t in tasks if t.status != "done"]
            if not pending:
                return "- No pending task -"
            result = "Your Pending Task:\n"
            for i, t in enumerate(pending):
                result += f"{i+1}. {t.title} (Priority: {t.priority}, Due: {t.due_date})\n)"
                return result

        elif action == "mark_done":
            index = data.get("index", 0)
            title_hint = data.get("title", "").lower()
            if title_hint:
                for i, t in enumerate(tasks):
                    if title_hint in t.title.lower():
                        tasks[i].mark_done()
                        save_tasks(tasks)
                        return f"=== Done: {tasks[i].title} ===\n"
            if 0 <= index < len(tasks):
                task = tasks[index].mark_done()
                save_tasks(tasks)
                return f"=== Done: {task[index].title} ===\n"
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

        elif action == "daily_briefing":
            return get_daily_briefing()

        elif action == "priority_summary":
            return get_priority_summary()

    except json.JSONDecodeError:
        return reply

