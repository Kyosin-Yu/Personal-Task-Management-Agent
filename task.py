#task class

"""
Code Explanations:
Task — is a blueprint for every task you create. Each task gets a unique id based on the current time
to_dict() — converts a task into a dictionary so it can be saved to JSON
__str__ — controls how a task looks when printed
"""

from datetime import datetime

class Task:
    def __init__(self,title, description="", due_date="", priority="medium"):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = "pending"

    def mark_done(self):
        self.status = "done"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    def __str__(self):
        return f"[{self.status.upper()}] {self.title} (Priority: {self.priority}), Due: {self.due_date}, Status: {self.status}]"