# Import Selenium's browser control tools
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import json


here = Path(__file__).parent
driver = webdriver.Chrome()

artist_name = "Aretha Franklin"
artist_url = "https://music.youtube.com/@Aretha"

driver.get(artist_url)


def find_albums_shelf(driver):
    """
    Find the carousel shelf containing Albums.

    Handles:
    1. Albums written directly inside an <a>
    2. Albums written inside <yt-formatted-string>
    """

    shelf_xpaths = [
        # Layout where the anchor itself contains the text Albums
        (
            "//ytmusic-carousel-shelf-renderer"
            "[.//a[translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz')='albums']]"
        ),

        # Layout where Albums is inside yt-formatted-string
        (
            "//ytmusic-carousel-shelf-renderer"
            "[.//yt-formatted-string["
            "translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz')='albums']]"
        ),
    ]

    for xpath in shelf_xpaths:
        shelves = driver.find_elements(By.XPATH, xpath)

        if shelves:
            return shelves[0]

    return False


try:
    # Wait until an Albums shelf exists in either layout
    album_shelf = WebDriverWait(driver, 20).until(find_albums_shelf)

    cards = album_shelf.find_elements(
        By.CSS_SELECTOR,
        "ytmusic-carousel ytmusic-two-row-item-renderer"
    )

    album_data = []

    for card in cards:
        lines = [
            line.strip()
            for line in card.text.splitlines()
            if line.strip()
        ]

        # Use find_elements so one bad card does not crash the script
        album_links = card.find_elements(
            By.CSS_SELECTOR,
            "a[href*='browse/']"
        )

        if not album_links:
            continue

        album_link = album_links[0]

        href = album_link.get_attribute("href")

        year = next(
            (
                int(line)
                for line in reversed(lines)
                if line.isdigit() and len(line) == 4
            ),
            None
        )

        title = (
            album_link.get_attribute("title")
            or album_link.text.strip()
        )

        # Sometimes the first anchor has no useful title.
        # Look through the other links if necessary.
        if not title:
            for link in album_links:
                possible_title = (
                    link.get_attribute("title")
                    or link.text.strip()
                )

                if possible_title:
                    title = possible_title
                    album_link = link
                    href = link.get_attribute("href")
                    break

        if title and year and href:
            album_data.append(
                {
                    "title": title,
                    "year": year,
                    "link": href,
                }
            )

    # Remove duplicate albums
    unique_albums = {}

    for album in album_data:
        key = (
            album["title"].lower(),
            album["year"],
        )

        unique_albums[key] = album

    album_data = list(unique_albums.values())

    album_data.sort(
        key=lambda album: (
            album["year"],
            album["title"].lower(),
        )
    )

    for album in album_data:
        print(album)

    # Save relative to this Python script, not the terminal location
    folder = here / "src" / "discographys" / artist_name
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"{artist_name}_disc.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            album_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print()
    print(f"Found {len(album_data)} albums.")
    print(f"Saved JSON to: {file_path.resolve()}")

except TimeoutException:
    print("Could not find the Albums shelf.")

finally:
    driver.quit()