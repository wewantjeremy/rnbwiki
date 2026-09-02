# Import Selenium's browser control tools
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pathlib import Path
from urllib.parse import quote_plus
import json
import unicodedata
import re



here = Path(__file__).parent

# Change this if this copy of the script is not inside your project's scripts folder.
with open(here / "../artists.json") as f:
    artists = json.load(f)
def normalize_name(name):
    name = unicodedata.normalize("NFKD", name)
    name = "".join(
        char for char in name
        if not unicodedata.combining(char)
    )

    name = name.casefold()

    name = re.sub(r"[^a-z0-9]+", " ", name)

    return " ".join(name.split())

def save_list(path, data):
    """Save review lists immediately so a later Selenium error does not lose them."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def find_exact_artist_link(driver, artist_name):
    """
    Search all YouTube Music channel results and return the channel link whose
    visible result text contains an exact line matching artist_name.

    This prevents examples such as:
      B5       -> The B-52s
      Babyface -> Babyface Ray
    """
    wanted = normalize_name(artist_name)

    try:
        channel_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a[href^='channel/']")
            )
        )
    except TimeoutException:
        return None

    for link in channel_links:
        try:
            # Search-result links normally live inside one of these result rows.
            row = link.find_element(
                By.XPATH,
                "./ancestor::ytmusic-responsive-list-item-renderer[1]"
            )
            lines = [
                normalize_name(line)
                for line in row.text.split("\n")
                if line.strip()
            ]

            if wanted in lines:
                return link

        except NoSuchElementException:
            # Some YouTube Music layouts put the channel link in a different
            # renderer. Fall back to the closest sizeable parent and inspect
            # its visible text instead of blindly accepting the link.
            try:
                parent = link.find_element(By.XPATH, "./ancestor::*[self::ytmusic-card-shelf-renderer or self::ytmusic-two-row-item-renderer or self::ytmusic-responsive-list-item-renderer][1]")
                lines = [
                    normalize_name(line)
                    for line in parent.text.split("\n")
                    if line.strip()
                ]
                if wanted in lines:
                    return link
            except NoSuchElementException:
                continue

    return None


def get_album_source(driver, artist_url, artist_name):
    """
    Return (source, layout_name).

    Large discography:
        Albums href -> Albums page -> grid

    Small discography:
        No Albums href/grid -> Albums carousel on artist page

    No album section:
        return (None, None)
    """

    # FIRST: try the separate Albums page / grid.
    album_page_url = None

    album_link_selectors = [
        (
            By.XPATH,
            "//yt-formatted-string[@role='heading']//a[normalize-space()='Albums']"
        )
    ]

    for by, selector in album_link_selectors:
        try:
            album_link = driver.find_element(by, selector)
            album_page_url = album_link.get_attribute("href")
            if album_page_url:
                break
        except NoSuchElementException:
            pass

    if album_page_url:
        driver.get(album_page_url)

        try:
            grid = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ytmusic-grid-renderer")
                )
            )
            print(f"{artist_name}: GRID")
            return grid, "grid"

        except TimeoutException:
            # We found an Albums href but did not get a grid. Return to the
            # artist page and try the carousel rather than killing the run.
            driver.get(artist_url)

    # SECOND: use the Albums carousel on the artist page.
    carousel_selectors = [
        (
            By.XPATH,
            "//ytmusic-carousel-shelf-renderer"
            "[.//yt-formatted-string[normalize-space()='Albums']]"
        ),
        (
            By.XPATH,
            "//ytmusic-carousel-shelf-renderer"
            "[.//a[normalize-space()='Albums']]"
        ),
    ]

    for by, selector in carousel_selectors:
        try:
            carousel = driver.find_element(by, selector)
            print(f"{artist_name}: CAROUSEL")
            return carousel, "carousel"
        except NoSuchElementException:
            pass

    return None, None


def scrape_album_source(source, layout):

    # ==========================================
    # GRID
    # ==========================================
    if layout == "grid":

        cards = source.find_elements(
            By.CSS_SELECTOR,
            "ytmusic-two-row-item-renderer"
        )

        album_data = []

        for card in cards:
            text_lines = [
                line.strip()
                for line in card.text.splitlines()
                if line.strip()
            ]

            title = text_lines[0] if text_lines else None

            year = None

            try:
                subtitle = card.find_element(
                    By.CSS_SELECTOR,
                    "yt-formatted-string.subtitle"
                )
                subtitle_text = subtitle.text.strip()

                if "Single" in subtitle_text:
                    continue

                spans = subtitle.find_elements(
                    By.CSS_SELECTOR,
                    "span"
                )

                for span in spans:
                    text = span.text.strip()

                    if text.isdigit() and len(text) == 4:
                        year = int(text)
                        break

            except:
                pass

            links = card.find_elements(
                By.CSS_SELECTOR,
                "a[href]"
            )

            href = next(
                (
                    link.get_attribute("href")
                    for link in links
                    if link.get_attribute("href")
                ),
                None
            )

            if title and href:
                album_data.append({
                    "title": title,
                    "year": year,
                    "link": href
                })

        album_data.sort(
            key=lambda album: album["year"]
        )

        return album_data
        # ==========================================
    # CAROUSEL
    # ==========================================
    if layout == "carousel":

        album_links = source.find_elements(
            By.CSS_SELECTOR,
            "a[href^='browse/']"
        )

        albums = {}

        for link in album_links:
            title = link.text.strip()
            href = link.get_attribute("href")

            if title and href:
                albums[href] = title

        texts = source.text.split("\n")

        years = [
            x.strip()
            for x in texts
            if x.strip().isdigit()
            and len(x.strip()) == 4
        ]

        album_data = []

        for (href, title), year in zip(
            albums.items(),
            years
        ):
            album_data.append({
                "title": title,
                "year": int(year),
                "link": href
            })

        album_data.sort(
            key=lambda album: album["year"]
        )

        return album_data

driver = webdriver.Chrome()

no_profile = []
no_albums = []

try:
    for artist in artists[542:]:
        artist_name = artist["name"]
        print(f"\n===== {artist_name} =====")

        search_url = (
            "https://music.youtube.com/search?q="
            + quote_plus(artist_name)
        )
        driver.get(search_url)

        # 1. FIND THE ACTUAL ARTIST, NOT THE FIRST CHANNEL RESULT.
        artist_link = find_exact_artist_link(driver, artist_name)

        if artist_link is None:
            print(f"{artist_name}: NO EXACT YOUTUBE MUSIC PROFILE")
            no_profile.append(artist_name)
            save_list(here / "no_profile.json", no_profile)
            continue

        artist_url = artist_link.get_attribute("href")
        print(f"{artist_name}: {artist_url}")
        driver.get(artist_url)

        # 2. GRID IF THERE IS A GRID; OTHERWISE ALBUMS CAROUSEL.
        album_source, layout = get_album_source(
            driver,
            artist_url,
            artist_name
        )

        if album_source is None:
            print(f"{artist_name}: PROFILE FOUND, BUT NO ALBUM SECTION")
            no_albums.append(artist_name)
            save_list(here / "no_albums.json", no_albums)
            continue

        # 3. SAME OUTPUT FORMAT REGARDLESS OF LAYOUT.
        album_data = scrape_album_source(album_source, layout)


        for album in album_data:
            print(album)

        folder = Path(f"src/discographys/{artist_name}")
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / f"{artist_name}_disc.json"

        with open(file_path, "w") as file:
            json.dump(album_data, file, indent=4)

        print(
            f"{artist_name}: saved {len(album_data)} albums "
            f"from {layout} -> {file_path}"
        )

finally:
    save_list(here / "no_profile.json", no_profile)
    save_list(here / "no_albums.json", no_albums)
    driver.quit()
