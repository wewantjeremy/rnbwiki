import requests
from bs4 import BeautifulSoup
import subprocess
import os
import time
import json
from pathlib import Path
import json
from urllib.parse import quote

here = Path(__file__).parent

with open(here / "artists.json") as f:
    artists = json.load(f)

headers = {
    "User-Agent": "rnb-wiki-image-scraper/0.1 (personal project; contact: seanjeremythaonly1left@gmail.com)"
}

def get_wiki_pic(url, name):


    folder = f"src/images/{name}"
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    images = soup.select('td.infobox-image img')

    for i, img in enumerate(images):
        srcset = img.get("srcset", "")
        actual_url = srcset.split(",")[-1].strip().split(" ")[0]
    if not img:
        print("no image found")
        return 
    
    actual_url = img.get("src")

    if actual_url.startswith("//"):
        actual_url = "https:" + actual_url

        subprocess.run([
            "curl",
            "-L"
            "-o",
            f"{folder}/{name}_{0}.jpg",
            actual_url
        ])

    print(f"complete: {name}")

for artist in artists[10:15]:
    name = artist['name']
    wiki_name = quote(name.replace(" ", "_"))
    get_wiki_pic(
        f"https://www.en.wikipedia.com/wiki/{wiki_name}",
        name
    )
    time.sleep(2)

'''import requests

def get_wiki_image(name):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "_")

    headers = {
        "User-Agent": "rnb-wiki-image-scraper/0.1 (personal project; contact: your@email.com)"
    }

    r = requests.get(url, headers=headers)
    print(r.status_code, r.text[:200])

    data = r.json()

    if "thumbnail" in data:
        print(data["thumbnail"]["source"])/*'''