from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from urllib.parse import quote
import json
import re


HERE = Path(__file__).resolve().parent
ARTISTS_FILE = HERE / "../artists.json"
OUTPUT_ROOT = HERE / "../discographys"

# Put direct YouTube Music artist URLs here for names that search gets wrong.
# You can add as many overrides as needed.
URL_OVERRIDES = {
    "Anthony Hamilton": "https://music.youtube.com/@AnthonyHamiltonOfficial",
    # "3T": "https://music.youtube.com/channel/CORRECT_3T_CHANNEL_ID",
}


def normalize_name(value):
    """Normalize artist names for exact result matching."""
    return " ".join(value.casefold().split())


def find_artist_url(driver, artist_name):
    """
    Use a direct URL override when available.
    Otherwise search YouTube Music and require an exact artist-name match.
    """
    if artist_name in URL_OVERRIDES:
        return URL_OVERRIDES[artist_name]

    search_url = f"https://music.youtube.com/search?q={quote(artist_name)}"
    driver.get(search_url)

    results = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a[href^='channel/'][aria-label]")
        )
    )

    wanted = normalize_name(artist_name)

    for result in results:
        result_name = result.get_attribute("aria-label") or ""

        if normalize_name(result_name) == wanted:
            artist_url = result.get_attribute("href")
            print(f"Matched {artist_name!r} to {result_name!r}")
            return artist_url

    found_names = [
        result.get_attribute("aria-label")
        for result in results
        if result.get_attribute("aria-label")
    ]

    raise RuntimeError(
        f"No exact YouTube Music artist match for {artist_name!r}. "
        f"Results included: {found_names}"
    )


def find_albums_shelf(driver):
    """Find the carousel whose header link says Albums."""
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//ytmusic-carousel-shelf-renderer"
                "[.//a[normalize-space()='Albums']]",
            )
        )
    )


def extract_album_data(album_shelf):
    """
    Extract title, year, and URL from each individual album card.
    This avoids separately collecting titles and years and then zipping them.
    """
    cards = album_shelf.find_elements(
        By.CSS_SELECTOR,
        "ytmusic-carousel ytmusic-two-row-item-renderer",
    )

    albums_by_url = {}

    for card in cards:
        lines = [
            line.strip()
            for line in card.text.splitlines()
            if line.strip()
        ]

        year = next(
            (
                int(line)
                for line in reversed(lines)
                if re.fullmatch(r"\d{4}", line)
            ),
            None,
        )

        # A card can contain multiple browse links, including an image link
        # with no visible title. Choose the first link with a usable title.
        title = None
        href = None

        for link in card.find_elements(By.CSS_SELECTOR, "a[href^='browse/']"):
            candidate_title = (
                link.get_attribute("title") or link.text
            ).strip()

            if candidate_title:
                title = candidate_title
                href = link.get_attribute("href")
                break

        if not title or not href:
            print(f"Skipping unreadable card: {lines}")
            continue

        if year is None:
            print(f"Skipping {title!r}: no four-digit year found in {lines}")
            continue

        albums_by_url[href] = {
            "title": title,
            "year": year,
            "link": href,
        }

    return sorted(
        albums_by_url.values(),
        key=lambda album: (album["year"], album["title"].casefold()),
    )


def save_discography(artist_name, album_data):
    """Write one JSON file after all albums have been extracted."""
    folder = OUTPUT_ROOT / artist_name
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"{artist_name}_disc.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            album_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Saved {len(album_data)} albums to {file_path}")


def main():
    with open(ARTISTS_FILE, encoding="utf-8") as file:
        artists = json.load(file)

    driver = webdriver.Chrome()
    failed_artists = []

    try:
        # Change this slice as needed.
        for artist in artists[38]:
            artist_name = artist["name"]
            print(f"\nProcessing {artist_name}")

            try:
                artist_url = find_artist_url(driver, artist_name)
                driver.get(artist_url)

                album_shelf = find_albums_shelf(driver)
                album_data = extract_album_data(album_shelf)

                if not album_data:
                    raise RuntimeError("Albums shelf was found, but no albums were extracted.")

                for album in album_data:
                    print(album)

                save_discography(artist_name, album_data)

            except Exception as error:
                print(f"FAILED {artist_name}: {error}")
                failed_artists.append({
                    "name": artist_name,
                    "error": str(error),
                })

    finally:
        driver.quit()

    if failed_artists:
        failed_path = OUTPUT_ROOT / "failed_artists.json"
        failed_path.parent.mkdir(parents=True, exist_ok=True)

        with open(failed_path, "w", encoding="utf-8") as file:
            json.dump(
                failed_artists,
                file,
                indent=4,
                ensure_ascii=False,
            )

        print(f"\nSaved failures to {failed_path}")


if __name__ == "__main__":
    main()
