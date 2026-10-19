
import json
import re
from pathlib import Path

INPUT_FILE = Path("articles_clean.json")
OUTPUT_FILE = Path("articles_chunks.json")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def clean_text(text):
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Avoid cutting words when possible
        if end < len(text):
            space_index = text.rfind(" ", start, end)
            if space_index > start:
                end = space_index

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        articles = json.load(file)

    all_chunks = []

    for article in articles:
        content = article.get("content", "")
        chunks = split_into_chunks(content)

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{len(all_chunks) + 1}",
                "url": article.get("url", ""),
                "title": article.get("title", ""),
                "chunk_index": index,
                "content": chunk
            })

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(all_chunks, file, ensure_ascii=False, indent=2)

    print("Articles processed:", len(articles))
    print("Total chunks:", len(all_chunks))
    print("Output saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
