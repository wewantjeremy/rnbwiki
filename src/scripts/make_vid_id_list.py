import os
import json

ids = []
base_path = "src/videoIds"
video_path = "src/videos/videos.txt"
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
                #print(video["id"])
                ids.append(video["id"])
with open(video_path, "a", encoding="utf-8") as f:
    json.dump(ids, f, indent=2)
                 