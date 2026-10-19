
import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

with open("article_urls.json", "r", encoding="utf-8") as file:
    urls = json.load(file)

output_file = Path("articles_sample.json")

session = requests.Session()
session.headers.update({
    "User-Agent": "AITechConsultantLearningProject/1.0"
})

results = []

for index, url in enumerate(urls[:5], start=1):
    print(f"\n[{index}/5] Fetching: {url}")

    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = (
            soup.find("h1")
            or soup.find("title")
        )
        title_text = title.get_text(" ", strip=True) if title else ""

        # Try common article-content containers.
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
                urljoin(url, img.get("src") or img.get("data-src"))
                for img in content.find_all("img")
                if img.get("src") or img.get("data-src")
            ]
        else:
            text = ""
            images = []

        results.append({
            "url": url,
            "title": title_text,
            "content": text,
            "images": images,
            "http_status": response.status_code,
        })

        print("Title:", title_text)
        print("Text characters:", len(text))
        print("Images found:", len(images))

    except requests.RequestException as error:
        print("Request failed:", error)

    # Be polite to the support website.
    if index < 5:
        time.sleep(2)

output_file.write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"\nSaved {len(results)} records to {output_file}")
