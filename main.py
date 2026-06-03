"""
Code Descriptions:
- App's control centre — it runs a loop that keeps asking what you want to do
- Can add, view, complete and delete tasks
- Every change is saved to tasks.json automatically
"""

from task import Task
from storage import save_tasks, load_tasks

def show_tasks(tasks):
    if not tasks:
        print('No tasks found')
        return
    for task in tasks:
        print(task)

def main():
    tasks = load_tasks()

    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. View All Task")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nChoose an option: ")

        if choice == '1':
            title = input("Task Title: ")
            description = input("Task Description: ")
            due_date = input("Task Due Date (e.g. 2024-12-31): ")
            priority = input("Task Priority (low/medium/high): ")
            task = Task(title, description, due_date, priority)
            tasks.append(task)
            save_tasks(tasks)
            print ("== Task Added ==")

        elif choice == '2':
            show_tasks(tasks)

        elif choice == '3':
            show_tasks(tasks)
            index = int(input("Enter Task number to mark done (1,2,3...): ")) - 1
            if 0 <= index < len(tasks):
                tasks[index].mark_done()
                save_tasks(tasks)
                print("== Task Marked as DONE ==")
            else:
                print("== Invalid Task Number ==")

        elif choice == '4':
            show_tasks(tasks)
            index = int(input("Enter Task number to mark done (1,2,3...): ")) - 1
            if 0 <= index < len(tasks):
                tasks.pop(index)
                save_tasks(tasks)
                print("== Task DELETED ==")
            else:
                print("== Invalid Task Number ==")

        elif choice == '5':
            print("== Program Terminated ==")
            break

        else:
            print("== Invalid Choice ==")

if __name__ == "__main__":
    main()
