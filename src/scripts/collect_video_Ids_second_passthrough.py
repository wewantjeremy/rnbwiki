import os
import json

base_path = "src/videoIds"

for root, dirs, files in os.walk(base_path):

    dirs.sort()   # makes folders alphabetical
    files.sort()  # makes files alphabetical

    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)

            print(path)

            with open(path) as f:
                videos = json.load(f)

            for video in videos:
                print(video["id"])