"""
Code Descriptions:
- App's control centre — it runs a loop that keeps asking what you want to do
- Can add, view, complete and delete tasks
- Every change is saved to tasks.json automatically
"""

from agent import chat

def main():
    print("[__Task Management Agents__]")
    print("="*30)
    print("How can I help you today? :")
    print("  - 'Add a task to study for finals tomorrow'")
    print("  - 'Show my tasks'")
    print("  - 'Mark task 1 as done'")
    print("  - 'What should I focus on today?'")
    print("=" * 30)
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Agent: Signing Off. Stay Productive! ")

        response = chat(user_input)
        print(f"\nAgent: {response}\n")

if __name__ == "__main__":
    main()
