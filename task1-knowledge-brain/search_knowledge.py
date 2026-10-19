
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="knowledge_articles"
)

print("Knowledge Brain is ready!")
print("Total chunks:", collection.count())

while True:
    question = input("\nAsk a question (or type exit): ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        results = collection.query(
            query_texts=[question],
            n_results=3
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not documents:
            print("No relevant articles found.")
            continue

        for i, document in enumerate(documents, start=1):
            metadata = metadatas[i - 1] or {}

            print(f"\n--- Result {i} ---")
            print("Title:", metadata.get("title", "Unknown"))
            print("URL:", metadata.get("url", ""))
            print("Content:", document)

    except Exception as error:
        print("Search error:", error)
