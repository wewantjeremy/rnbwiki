from scrapeBioObscure import scrape2
from scrapeBioWikipedia import scrape1
from scrape_last_fm import scrape3
from pathlib import Path

all_bios = {}

for source_name, scraper in [
    ("Wikipedia", scrape1),
    ("Rare & Obscure", scrape2),
    ("Last.fm", scrape3),
]:
    print(f"Trying {source_name}")
    results = scraper()

    for artist_name, text in results:
        all_bios.setdefault(artist_name, [])
        all_bios[artist_name].append((source_name, text))

for artist_name, bios in all_bios.items():
    source_name, best_text = max(bios, key=lambda item: len(item[1]))

    folder = Path(f"src/bios/{artist_name}")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"{artist_name}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(best_text)

    print(f"{artist_name}: kept {source_name} bio")