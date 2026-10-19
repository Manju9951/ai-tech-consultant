
import json
from pathlib import Path

file_path = Path("articles_progress.jsonl")

count = 0
empty_content = 0

with file_path.open("r", encoding="utf-8") as file:
    for line in file:
        try:
            record = json.loads(line)
            count += 1

            if not record.get("content", "").strip():
                empty_content += 1

        except json.JSONDecodeError:
            print("Warning: Invalid JSON line found")

print("Total saved records:", count)
print("Records with empty content:", empty_content)
