
import json
import time
import xml.etree.ElementTree as ET

import requests

SITEMAP_URL = (
    "https://support.brilliantdirectories.com/support/sitemap.xml"
)

HEADERS = {
    "User-Agent": "AITechConsultantLearningProject/1.0"
}


def get_sitemap_urls(sitemap_url):
    print(f"Reading sitemap: {sitemap_url}")

    response = requests.get(
        sitemap_url,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)

    entries = []
    for element in root.iter():
        if element.tag.endswith("}loc") or element.tag == "loc":
            if element.text:
                entries.append(element.text.strip())

    return entries


def main():
    try:
        entries = get_sitemap_urls(SITEMAP_URL)

        # Sitemap index files contain links to other sitemap files.
        sitemap_files = [
            url for url in entries
            if url.lower().endswith(".xml")
        ]

        article_urls = [
            url for url in entries
            if not url.lower().endswith(".xml")
        ]

        for sitemap_url in sitemap_files:
            time.sleep(1)
            child_entries = get_sitemap_urls(sitemap_url)

            for url in child_entries:
                if not url.lower().endswith(".xml"):
                    article_urls.append(url)

        article_urls = sorted(set(article_urls))

        with open(
            "sitemap_urls.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                article_urls,
                file,
                indent=2,
                ensure_ascii=False,
            )

        print(f"URLs collected: {len(article_urls)}")
        print("Saved to sitemap_urls.json")
        print("Sample URLs:")

        for url in article_urls[:10]:
            print(url)

    except requests.RequestException as error:
        print(f"Network or HTTP error: {error}")
    except ET.ParseError as error:
        print(f"Could not parse sitemap XML: {error}")


if __name__ == "__main__":
    main()
