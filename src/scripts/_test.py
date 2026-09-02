from pathlib import Path
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


ARTIST_URL = "https://music.youtube.com/@Aretha"


def find_albums_link(driver):
    """
    Find the Albums navigation link across multiple YouTube Music layouts.
    Returns a WebElement or None.
    """

    selectors = [
        # Albums text nested inside yt-formatted-string
        (
            By.XPATH,
            "//a[.//yt-formatted-string["
            "translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz')='albums']]"
        ),

        # Albums text directly inside an anchor
        (
            By.XPATH,
            "//a["
            "translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz')='albums']"
        ),

        # Fallback: any anchor containing an Albums browse link
        (
            By.XPATH,
            "//a[contains(@href, 'browse/') "
            "and contains("
            "translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), "
            "'albums')]"
        ),
    ]

    for by, selector in selectors:
        elements = driver.find_elements(by, selector)

        for element in elements:
            if element.is_displayed():
                return element

    return None


def open_albums_page(driver):
    albums_link = WebDriverWait(driver, 20).until(
        lambda d: find_albums_link(d)
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        albums_link
    )

    driver.execute_script("arguments[0].click();", albums_link)

        (
            By.CSS_SELECTOR,
            "ytmusic-carousel-shelf-renderer"
        ),
    ]

    for by, selector in possible_containers:
        containers = driver.find_elements(by, selector)

        for container in containers:
            text = container.text.lower()

            if "album" in text:
                return container

    raise RuntimeError("Could not find an album container.")


def scrape_album_cards(album_container):
    cards = album_container.find_elements(
        By.CSS_SELECTOR,
        "ytmusic-two-row-item-renderer"
    )

    albums = []

    for card in cards:
        text_lines = [
            line.strip()
            for line in card.text.splitlines()
            if line.strip()
        ]

        links = card.find_elements(By.CSS_SELECTOR, "a[href]")

        if not text_lines or not links:
            continue

        title = text_lines[0]

        href = next(
            (
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
            ),
            None
        )

        year = next(
    (
        int(line)                 # ← cast to int here
        for line in text_lines[1:]
        if line.isdigit() and len(line) == 4
    ),
    None,
)

        albums.append(
            {
                "title": title,
                "year": year,
                "url": href,
                "raw_text": text_lines,
            }
        )

    return albums


def main():
    driver = webdriver.Chrome()

    try:
        driver.get(ARTIST_URL)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "ytmusic-app")
            )
        )

        open_albums_page(driver)

        album_container = find_album_container(driver)

        albums = scrape_album_cards(album_container)
        albums.sort(
    key=lambda a: (
        a["year"] is None,        # albums with no year go last
        a["year"] if a["year"] is not None else 9999
    )
)
        
        print(f"Found {len(albums)} albums")

        for album in albums:
            print(album)

        folder = Path("src/discographys/Aretha Franklin")
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / "Aretha Franklin_disc.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(albums, file, indent=4, ensure_ascii=False)

    except TimeoutException:
        print("Timed out while looking for the Albums page or album shelf.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()