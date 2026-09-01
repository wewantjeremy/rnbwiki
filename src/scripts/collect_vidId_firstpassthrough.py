import os
import json

base_path = "src/videoIds"

for artist in os.listdir(base_path):
    artist_path = os.path.join(base_path, artist)
    if not os.path.isdir(artist_path):
                continue
    path = os.path.join(artist_path, f"{artist}_videos.json")
    with open(path) as f:
        videos = json.load(f)
    for video in videos:
      print(video["id"])
'''for video_id in video_ids:
    print(video_id)

for channel in channels:

    folder = f"downloads/{channel['name']}"
    os.makedirs(folder, exist_ok=True)

    for video_id in channel["videoIds"]:
        url = f"https://www.youtube.com/watch?v={video_id}"

        # yt-dlp download'''