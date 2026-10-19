

import json
from collections import Counter

with open("sitemap_urls.json", "r", encoding="utf-8") as file:
    urls = json.load(file)

counts = Counter()

articles = []
folders = []

for url in urls:
    if "/support/solutions/articles/" in url:
        counts["articles"] += 1
        articles.append(url)
    elif "/support/solutions/folders/" in url:
        counts["folders"] += 1
        folders.append(url)
    elif url.rstrip("/").endswith("/support/solutions"):
        counts["solution_home"] += 1
    elif url.rstrip("/").endswith("/support/home"):
        counts["home"] += 1
    else:
        counts["other"] += 1

print("Total URLs:", len(urls))
print("\nURL categories:")

for category, count in counts.items():
    print(f"{category}: {count}")

print("\nSample article URLs:")
for url in articles[:10]:
    print(url)

print("\nSample folder URLs:")
for url in folders[:5]:
    print(url)

with open("article_urls.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, indent=2, ensure_ascii=False)

print(f"\nSaved {len(articles)} article URLs to article_urls.json")
