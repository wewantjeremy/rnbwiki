import os
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
discography_dir = HERE / "discographys"

with open(HERE / "artists.json", "r") as f:
    artists = json.load(f)

json_artists = {artist["name"] for artist in artists}

folder_artists = {
    folder.name
    for folder in discography_dir.iterdir()
    if folder.is_dir()
}

missing = sorted(json_artists - folder_artists)

print(f"Missing: {len(missing)}")
for artist in missing:
    print(artist)