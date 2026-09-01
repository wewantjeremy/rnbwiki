import pyperclip
import re
import requests
from bs4 import BeautifulSoup
import json
import os
from pathlib import Path


def scrape2():
    here = Path(__file__).parent

    with open(here / "../artists.json") as f:
        artists = json.load(f)

    def scrapeObscureBio(url, name):
        folder = f"src/bios/{name}"
        os.makedirs(folder, exist_ok=True)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        content = soup.find("div", id="content")

        if content is None:
            print(f"Couldn't find content on {url}")
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
        text = re.sub(r"\n{3,}", "\n", text)
        text = re.sub(r"([(\[])\s+", r"\1", text)
        text = re.sub(r"\s+([,.;:!?)\]])", r"\1", text)
        text = text.replace("\\\\", "/")

        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        if paragraphs:
            text = "\n".join("\t" + p for p in paragraphs)

        folder = f"src/bios/{name}"
        file_path = Path(folder) / f"{name}.txt"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        print(url)
        return text

    bios = []

    for artist in artists[120:]:
        search_name = re.sub(r"\s", "-", artist["name"])

        try:
            text = scrapeObscureBio(
                f"https://rareandobscuremusic.wordpress.com/{search_name}",
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
