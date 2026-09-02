from pathlib import Path
import json
import sys


SRC = Path(__file__).resolve().parents[1]

BIOS_DIR = SRC / "bios"
IMAGES_DIR = SRC / "images"
VIDEOS_DIR = SRC / "videoIds"
DISCOG_DIR = SRC / "discographys"
DATA_DIR = SRC / "data"

DATA_DIR.mkdir(exist_ok=True)

def js_string(value):
    return json.dumps(str(value), ensure_ascii=False)


def find_file(folder, patterns):
    
    if not folder.exists():
        return None

    for pattern in patterns:
        matches = sorted(
            p for p in folder.glob(pattern)
            if p.is_file() and not p.name.endswith("~")
        )

        if matches:
            return matches[0]

    return None


    folder = DISCOG_DIR / artist

    disc_file = find_file(folder, [
        f"{artist}_disc.json",
        "*_disc.json",
        "*.json",
    ])

    if not disc_file:
        print(f"  ⚠ no discography: {artist}")
        return []

    try:
        data = json.loads(
            disc_file.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as e:
        print(f"  ❌ broken discography JSON: {artist}: {e}")
        return []


    if isinstance(data, dict):
        data = data.get("albums", [])

    if not isinstance(data, list):
        print(f"  ⚠ unknown discography format: {artist}")
        return []

    albums = []

    for album in data:
        if not isinstance(album, dict):
            continue

        title = album.get("title")
        year = album.get("year")
        link = album.get("link")

        if not title:
            continue

        albums.append({
            "title": title,
            "year": year,
            "link": link,
        })

    return albums

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif",
}

def load_biography(artist):
    path = BIOS_DIR / artist / f"{artist.lower()}.txt"

    # Account for filenames whose capitalization differs
    if not path.exists():
        txt_files = list((BIOS_DIR / artist).glob("*.txt"))
        if not txt_files:
            raise FileNotFoundError(f"No biography for {artist}")
        path = txt_files[0]

    with open(path, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip()
        ]


def load_videos(artist):
    path = VIDEOS_DIR / artist / f"{artist}_videos.json"

    with open(path, encoding="utf-8") as f:
        videos = json.load(f)

    return [video["id"] for video in videos]


def load_discography(artist):
    path = DISCOG_DIR / artist / f"{artist}_disc.json"

    with open(path, encoding="utf-8") as f:
        return json.load(f)
def load_images(artist):
    folder = IMAGES_DIR / artist

    if not folder.exists():
        print(f"  ⚠ no images: {artist}")
        return []

    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

    files = [
        p for p in folder.iterdir()
        if p.is_file()
        and p.suffix.lower() in image_extensions
        and not p.name.startswith(".")
    ]

    files.sort(key=lambda p: p.name.lower())

    return [
        f"/src/images/{artist}/{p.name}"
        for p in files
    ]
def format_string_array(values, indent="    "):
    if not values:
        return "[]"

    lines = ["["]

    for value in values:
        lines.append(
            f"{indent}{js_string(value)},"
        )

    lines.append("  ]")

    return "\n".join(lines)


def format_biography(paragraphs):
    if not paragraphs:
        return "[]"

    lines = ["["]

    for paragraph in paragraphs:
        lines.append(
            f"    {{ text: {js_string(paragraph)}, indent: true }},"
        )

    lines.append("  ]")

    return "\n".join(lines)


def format_albums(albums):
    if not albums:
        return "[]"

    lines = ["["]

    for album in albums:
        parts = [
            f"title: {js_string(album['title'])}"
        ]

        if album.get("year") is not None:
            try:
                year = int(album["year"])
                parts.append(f"year: {year}")
            except (ValueError, TypeError):
                parts.append(
                    f"year: {js_string(album['year'])}"
                )

        if album.get("link"):
            parts.append(
                f"link: {js_string(album['link'])}"
            )

        lines.append(
            "    { " + ", ".join(parts) + " },"
        )

    lines.append("  ]")

    return "\n".join(lines)

def compile_artist(artist):
    print(f"Compiling {artist}...")

    images = load_images(artist)
    videos = load_videos(artist)
    biography = load_biography(artist)
    albums = load_discography(artist)

    output = f"""export default {{
  id: {js_string(artist)},
  name: {js_string(artist)},

  images: {format_string_array(images)},

  videoIds: {format_string_array(videos)},

  biography: {format_biography(biography)},

  albums: {format_albums(albums)}
}}
"""

    destination = DATA_DIR / f"{artist}.js"
    destination.write_text(
        output,
        encoding="utf-8"
    )

    print(
        f" {len(images)} images"
        f" {len(videos)} videos"
        f" {len(biography)} bio paragraphs"
        f" {len(albums)} projects"
    )


def get_artists():
    """
    Use the union of the artist folders.

    This means an artist still gets compiled even if they're
    missing one category.
    """

    artists = set()

    for root in (
        BIOS_DIR,
        IMAGES_DIR,
        VIDEOS_DIR,
        DISCOG_DIR,
    ):
        if not root.exists():
            continue

        for folder in root.iterdir():
            if folder.is_dir() and not folder.name.startswith("."):
                artists.add(folder.name)

    return sorted(artists, key=str.casefold)

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, text):
        for f in self.files:
            f.write(text)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

def main():

    artists = get_artists()
    with open("compile.txt", "w") as log:
        old_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log)

        try:
            print(f"\nFound {len(artists)} artists.\n")

            for artist in artists:
                if artist == "112":
                    print("skipped 112")
                    continue

                try:
                    compile_artist(artist)
                except Exception as e:
                    print(f"FAILED {artist}: {e}")

            print("\nDone.")
        finally:
            sys.stdout = old_stdout


if __name__ == "__main__":
    main()