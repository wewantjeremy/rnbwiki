from dotenv import load_dotenv
import os
from pyyoutube import Api
from pathlib import Path
import json

def scrape_videos():
  root_dir = Path(__file__).resolve().parent.parent.parent
  json_dir = Path(__file__).resolve().parent.parent
  env_path = root_dir / '.env'
  with open(json_dir / "artists.json") as f:
          artists = json.load(f)
  load_dotenv(dotenv_path=env_path)
  api = Api(api_key=os.getenv("API_KEY"))

  for artist in artists[514:]:
    artist_name = artist["name"]  
    response = api.search_by_keywords(
      q = f"{artist_name} music video",
      search_type = ["video"],
      count = 20
    )
    videos = []

    for v in response.items:
        if "Audio" in v.snippet.title: 
            continue
        if "Visualizer" in v.snippet.title: 
            continue
        if "Lyric Video" in v.snippet.title:
            continue
        videos.append({
            "id": v.id.videoId,
            "title": v.snippet.title
        })
    folder = Path(f"src/videoIds/{artist_name}")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"{artist_name}_videos.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(videos, file, indent=2, ensure_ascii=False)
scrape_videos()

