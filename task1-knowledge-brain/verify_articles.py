
import json
from pathlib import Path

input_file = Path("articles_progress.jsonl")

records = []

with input_file.open("r", encoding="utf-8") as file:
    for line in file:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

unique = {}

for record in records:
    url = record.get("url")
    if url:
        unique[url] = record

empty_content = [
    r for r in unique.values()
    if not r.get("content", "").strip()
]

empty_title = [
    r for r in unique.values()
    if not r.get("title", "").strip()
]

print("Total saved records:", len(records))
print("Unique article URLs:", len(unique))
print("Duplicate records:", len(records) - len(unique))
print("Empty content:", len(empty_content))
print("Empty titles:", len(empty_title))

if unique:
    sample = next(iter(unique.values()))
    print("\nSample article:")
    print("Title:", sample.get("title"))
    print("URL:", sample.get("url"))
    print("Content characters:", len(sample.get("content", "")))
    print("Images:", len(sample.get("images", [])))

Path("articles_clean.json").write_text(
    json.dumps(
        list(unique.values()),
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print("\nClean data saved to articles_clean.json")
