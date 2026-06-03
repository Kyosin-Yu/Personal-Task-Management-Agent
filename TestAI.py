from aiHelper import parse_task_from_input, suggest_priority

print("=== Testing AI Parse ===")
print("=" * 40)
result = parse_task_from_input("Remind me to study for my finals next Monday")
print(result)
print("=" * 40)

result2 = suggest_priority("Study for finals","Need to cover 5 chapter before exam")
print(result2)