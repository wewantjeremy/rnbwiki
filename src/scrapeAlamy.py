import requests
from bs4 import BeautifulSoup
import subprocess
import os
import time
import json
from pathlib import Path
import json

here = Path(__file__).parent

with open(here / "artists.json") as f:
    artists = json.load(f)

headers = {"User-Agent": "Mozilla/5.0"}


def get_one_alamy(url):
    folder = "images"
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    images = soup.select('div[data-testid^="search-tile"] img')

    for i, img in enumerate(images):
        path = f"{folder}/alamy_{i}.jpg"

        if os.path.exists(path):
            print("already exists, skipping:", path)
            continue

        src = img.get("srcset", "")
        actual_url = src.split(",")[-1].strip().split(" ")[0]

        subprocess.run(["curl", "-L", "-o", path, actual_url])

    print("complete")


text = input("Enter a url: ")
get_one_alamy(text)
