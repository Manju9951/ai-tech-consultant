
import requests
from bs4 import BeautifulSoup

url = "https://support.brilliantdirectories.com/support/solutions/12000001522"

headers = {
    "User-Agent": "AITechConsultantLearningProject/1.0"
}

response = requests.get(url, headers=headers, timeout=30)

print("Status code:", response.status_code)
print("Final URL:", response.url)

soup = BeautifulSoup(response.text, "html.parser")

print("\nPAGE TITLE:")
print(soup.title.get_text(strip=True) if soup.title else "No title")

print("\nMAIN HEADINGS:")
for heading in soup.find_all(["h1", "h2", "h3"])[:15]:
    print(heading.get_text(" ", strip=True))

print("\nLINKS CONTAINING 'solution' OR 'article':")
count = 0

for link in soup.find_all("a", href=True):
    href = link["href"]
    text = link.get_text(" ", strip=True)

    if "solution" in href.lower() or "article" in href.lower():
        print(text[:100], "->", href)
        count += 1

        if count >= 20:
            break
