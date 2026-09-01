import os
import json
from pathlib import Path

here = Path(__file__).parent

with open(here / "artists.json") as f:
    artists = json.load(f)


def nameChanger(name):
    folder = f"src/images/{name}"

    files = sorted(os.listdir(folder))
    for name in images:
        for i, filename in enumerate(files, start=1):
            old_path = os.path.join(folder, filename)

            # skip folders
            if not os.path.isfile(old_path):
                continue

            # keep original extension
            extension = os.path.splitext(filename)[1]

            new_name = f"Brandy_{i}{extension}"
            new_path = os.path.join(folder, new_name)

            os.rename(old_path, new_path)

            print(f"{filename} -> {new_name}")
