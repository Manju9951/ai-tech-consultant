
import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URLS_FILE = Path("article_urls.json")
OUTPUT_FILE = Path("articles_progress.jsonl")
BATCH_SIZE = 50

urls = json.loads(URLS_FILE.read_text(encoding="utf-8"))

# Skip URLs already saved successfully.
completed = set()

if OUTPUT_FILE.exists():
    with OUTPUT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)
                if record.get("content") and record.get("title"):
                    completed.add(record["url"])
            except json.JSONDecodeError:
                continue

pending = [url for url in urls if url not in completed]
batch = pending[:BATCH_SIZE]

print("Total article URLs:", len(urls))
print("Already saved:", len(completed))
print("Remaining:", len(pending))
print("This batch:", len(batch))

headers = {
    "User-Agent": "AITechConsultantLearningProject/1.0"
}

with requests.Session() as session:
    session.headers.update(headers)

    for index, url in enumerate(batch, start=1):
        print(f"\n[{index}/{len(batch)}] {url}")

        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title_element = soup.find("h1") or soup.find("title")
            title = (
                title_element.get_text(" ", strip=True)
                if title_element else ""
            )

            content = (
                soup.select_one(".article-body")
                or soup.select_one(".solution-article")
                or soup.select_one("article")
                or soup.select_one("main")
                or soup.body
            )

            if content:
                for element in content.select(
                    "script, style, nav, footer, header"
                ):
                    element.decompose()

                text = content.get_text(" ", strip=True)

                images = [
                    {
                        "url": urljoin(
                            url, img.get("src") or img.get("data-src")
                        ),
                        "alt": img.get("alt", "")
                    }
                    for img in content.find_all("img")
                    if img.get("src") or img.get("data-src")
                ]
            else:
                text = ""
                images = []

            record = {
                "url": url,
                "title": title,
                "content": text,
                "images": images,
                "http_status": response.status_code
            }

            # Save each successful article immediately.
            with OUTPUT_FILE.open("a", encoding="utf-8") as file:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")

            if title and text:
                completed.add(url)
                print("Saved:", title)
                print("Characters:", len(text), "| Images:", len(images))
            else:
                print("Warning: title or content is empty; check this page.")

        except requests.RequestException as error:
            print("Request failed:", error)

        time.sleep(2)

print("\nBatch finished.")
print("Successfully saved:", len(completed))
print("Remaining to retry/process:", len(urls) - len(completed))
print("Output file:", OUTPUT_FILE)
