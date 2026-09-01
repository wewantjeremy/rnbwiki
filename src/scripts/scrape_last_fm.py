import re
import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path


def scrape3():
    here = Path(__file__).parent

    with open(here / "../artists.json") as f:
        artists = json.load(f)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def scrape_fm(url, name):
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        content = soup.find("div", class_="wiki-content")

        if content is None:
            print(f"Couldn't find Last.fm content on {url}")
            return None

        paragraphs = content.find_all("p")

        text = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if p.get_text(" ", strip=True)
        )

        text = re.sub(r"\[\s*\d+\s*\]", "", text)
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)
        text = re.sub(r'"\s*(.*?)\s*"', r'"\1"', text)
        text = re.sub(r"\s+'\s*", "'", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"([(\[])\s+", r"\1", text)
        text = re.sub(r"\s+([,.;:!?)\]])", r"\1", text)

        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        text = "\n\n".join("\t" + p for p in paragraphs)

        return text

    bios = []

    for artist in artists[120:]:
        search_name = re.sub(r"\s", "+", artist["name"])

        try:
            text = scrape_fm(
                f"https://www.last.fm/music/{search_name}/+wiki/",
                artist["name"]
            )

            if text:
                bios.append((artist["name"], text))

        except requests.exceptions.HTTPError:
            print(f"Skipping {artist['name']}: page not found")
            continue

        except Exception as error:
            print(f"Skipping {artist['name']}: {error}")
            continue

    return bios