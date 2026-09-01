
from dotenv import load_dotenv
import os
from pyyoutube import Api
from pathlib import Path
import json

def scrape_discography():
  root_dir = Path(__file__).resolve().parent.parent.parent
  json_dir = Path(__file__).resolve().parent.parent
  env_path = root_dir / '.env'
  with open(json_dir / "artists.json") as f:
          artists = json.load(f)
  load_dotenv(dotenv_path=env_path)
  api = Api(api_key=os.getenv("API_KEY"))

  for artist in artists[:10]:
    artist_name = artist["name"]  
    response = api.search_by_keywords(
      q = f"{artist_name}",
      search_type = ["channel"],
      count = 5
    )
    channels = []

    for c in response.items:
      channels.append({
         "title": c.snippet.title,
          "channel_id": c.id.channelId,
         # "url": c.url
      })
    folder = Path(f"src/channels/{artist_name}")
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"{artist_name}_channels.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(channels, file, indent=2, ensure_ascii=False)
scrape_discography()