import json
import os

with open("artists.json") as f:
    artists = json.load(f)

for artist in artists:
    name = artist["name"]
    with open(f"images/{name}/images.json") as f:
        images = json.load(f)

    with open(f"bios/{name}.json") as f:
        bio = json.load(f)

    with open(f"videoIds/{name}.json") as f:
        videoIds = json.load(f)

    with open(f"discography/{name}.json") as f:
        albums = json.load(f)

    artist_page = {
        "id": artist["id"],
        "name": name,
        "images": images,
        "videoIds": videoIds,
        "biography": bio,
        "albums": albums
    }

    with open(f"src/artists/{name}.js", "w") as f:
        f.write(
            "export default "
            + json.dumps(artist_page, indent=2)
        )