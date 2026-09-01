import json
import json_repair
import os

folder = "src/videoIds"

for filename in os.listdir(folder):
        artist_path = os.path.join(folder, filename)
        if not os.path.isdir(artist_path):
             continue
        path = os.path.join(folder, filename, f"{filename}_videos.json")
        with open(path, "r") as f:
            repaired = json_repair.loads(f.read())
        with open(path, "w") as f:
              json.dump(repaired, f, indent=2)
        print(f"✅ fixed {filename}")
