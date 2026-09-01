import re
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path


def clean_text(text):
    text = re.sub(r"\[\s*\d+\s*\]", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r'"\s*(.*?)\s*"', r'"\1"', text)
    text = re.sub(r"\s+'\s*", "'", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n", text)
    text = re.sub(r"([(\[])\s+", r"\1", text)
    text = re.sub(r"\s+([,.;:!?)\]])", r"\1", text)

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return "\n".join("\t" + p for p in paragraphs)


def scrape1():
    here = Path(__file__).parent

    with open(here / "../artists.json") as f:
        artists = json.load(f)

    headers = {"User-Agent": "Mozilla/5.0"}
    bios = []

    def scrapeBio(url):
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find("div", id="mw-content-text")

        if content is None:
            raise ValueError("No Wikipedia content found")

        paragraphs = content.find_all("p")

        text = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if p.get_text(" ", strip=True)
        )

        if re.search(r"may refer to:", text[:300], re.IGNORECASE):
            raise ValueError("Disambiguation page")

        if re.search(r"does not exist|Did you mean:", text[:500], re.IGNORECASE):
            raise ValueError("Missing/search page")

        return clean_text(text)

    for artist in artists[120:]:
        original_name = artist["name"]
        name = re.sub(r"'\s+", "'", original_name)
        new_name = name.replace("'", "%27").replace(" ", "_")

        urls = [
            f"https://en.wikipedia.org/wiki/{new_name}",
            f"https://en.wikipedia.org/wiki/{new_name}_(band)",
            f"https://en.wikipedia.org/wiki/{new_name}_(group)",
            f"https://en.wikipedia.org/wiki/{new_name}_(singer)",
            f"https://en.wikipedia.org/wiki/{new_name}_(musician)",
        ]

        for url in urls:
            try:
                print("Trying:", url)
                text = scrapeBio(url)
                bios.append((original_name, text))
                print("Saved:", original_name)
                break

            except requests.exceptions.HTTPError:
                print("404:", url)
                continue

            except ValueError as error:
                print(f"Skipping URL for {original_name}: {error}")
                continue

            except Exception as error:
                print(f"Error for {original_name} at {url}: {error}")
                break

    return bios