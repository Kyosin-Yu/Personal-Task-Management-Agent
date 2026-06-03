#saving/loading tasks to a file
"""
Code Descriptions;
save_tasks() — takes all your tasks and writes them into tasks.json
load_tasks() — reads tasks.json and brings your tasks back into the app
task_from_dict() — converts raw JSON data back into a proper Task object
The try/except means if tasks.json is empty or missing, it just returns an empty list instead of crashing
"""


import json
from task import Task

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return [task_from_dict(d) for d in data]
    except:
        return []

def task_from_dict(d):
    task = Task(d["title"], d["description"], d["due_date"], d["priority"])
    task.id = d["id"]
    task.status = d["status"]
    return task
