#enhancement from reactive to proactive

from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from storage import load_tasks
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

def get_overdue_tasks():
    tasks = load_tasks()
    today = datetime.now().date()
    overdue = []
    for task in tasks:
        if task.due_date and task.status == "pending":
            try:
                due = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                if due < today:
                    overdue.append(task)
            except:
                pass
    return overdue

def get_daily_briefing():
    tasks = load_tasks()
    today = datetime.now().strftime("%Y-%m-%d")
    overdue = get_overdue_tasks()

    pending = [t for t in tasks if t.status == "pending"]
    done = [t for t in tasks if t.status == "done"]

    task_info = "\n".join([
        f"- {t.title} (Priority: {t.priority}, Due: {t.due_date})"
        for t in pending
    ]) or "== No pending tasks =="

    overdue_info = "\n".join([
        f"- {t.title} (Due: {t.due_date})"
        for t in overdue
    ]) or "None"

    prompt = f"""Today is {today},

Here is your Pending Tasks:
{task_info}

Overdue Tasks:
{overdue_info}

Completed tasks today: {len(done)}

Give a friendly daily briefing. Include:
1. A quick summary of their workload
2. Which tasks to focus on today (top 3)
3. A reminder about overdue tasks if any
4. A short motivational message

Keep it concise and friendly //>u<//"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def score_tasks():
    tasks = load_tasks()
    today = datetime.now().date()

    priority_score = {"high": 3,"medium": 2,"low": 1}
    scored=[]

    for task in tasks:
        if task.status == "pending":
            score = priority_score.get(task.priority, 1)
            if task.due_date:
                try:
                    due = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    days_left = (due - today).days
                    if days_left < 0:
                        score += 5
                    elif days_left == 0:
                        score += 4
                    elif days_left <= 2:
                        score += 3
                    elif days_left <= 7:
                        score += 2
                except:
                    pass
            scored.append((task, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

def get_priority_summary():
    scored = score_tasks()
    if not scored:
        return "== No pending tasks to rank =="

    result = "-- Task Priority Ranking --\n"
    for i, (task, score) in enumerate(scored):
        result += f"{i+1}. {task.title} (Due: {task.due_date}, Priority: {task.priority}, Score: {score})\n"
    return result
