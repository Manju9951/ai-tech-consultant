
import json
import chromadb
from pathlib import Path

INPUT_FILE = Path("articles_chunks.json")
DB_PATH = Path("chroma_db")
COLLECTION_NAME = "knowledge_articles"
BATCH_SIZE = 100

def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        collection.upsert(
            ids=[item["chunk_id"] for item in batch],
            documents=[item["content"] for item in batch],
            metadatas=[
                {
                    "url": item["url"],
                    "title": item["title"],
                    "chunk_index": item["chunk_index"]
                }
                for item in batch
            ]
        )

        print(
            f"Indexed {min(start + len(batch), len(chunks))}"
            f"/{len(chunks)} chunks"
        )

    print("\nIndexing completed!")
    print("Total stored chunks:", collection.count())
    print("Database location:", DB_PATH.resolve())


if __name__ == "__main__":
    main()
