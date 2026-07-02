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

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_getty(url, name):
    folder = f"src/images/{name}"
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    images = soup.select('source[data-testid="asset-picture-source"]')

    for i, img in enumerate(images):
        path = f"{folder}/{name}_{i}.jpg"

        if os.path.exists(path):
            print("already exists, skipping:", path)
            continue

        srcset = img.get("srcset", "")
        actual_url = srcset.split(",")[-1].strip().split(" ")[0]

        subprocess.run([
            "curl",
            "-L",
            "-o",
            path,
            actual_url
        ])

    print(f"complete: {name}")

for artist in artists[100:200]:
    #text = input(f"{artist['name']}: artist or group? ").lower()
    #if text == "group":
    #    get_getty(f"https://www.gettyimages.com/search/2/image?phrase={artist['name']}%20r%26b%20group", artist['name'])
    #    time.sleep(2)
    #elif text == "artist":
        get_getty(f"https://www.gettyimages.com/search/2/image?phrase={artist['name']}", artist['name'])
    #else:
    #    print("please enter a valid response")
    #    continue