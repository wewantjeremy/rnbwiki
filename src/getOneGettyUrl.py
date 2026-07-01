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

def get_one_getty(url):
    folder = "src/images/new"
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    images = soup.select('source[data-testid="asset-picture-source"]')
  

    for i, img in enumerate(images):
        path = f"{folder}/getty_{i}.jpg"

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

    print("complete")

text = input("Enter a url: ")
get_one_getty(text)
  