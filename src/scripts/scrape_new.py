# Import Selenium's browser control tools
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
import json
from urllib.parse import quote

here = Path(__file__).parent
driver = webdriver.Chrome()

driver.get("https://music.youtube.com/@Babyface")

link2 = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR,"ytmusic-carousel a[href^='browse/']")
    )
)


albums_header = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//ytmusic-carousel-shelf-renderer"
            "[.//a[normalize-space()='Albums']]"
        )
    )
)

album_shelf = albums_header

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

    album_link = card.find_element(
        By.CSS_SELECTOR,
        "a[href^='browse/']"
    )

    href = album_link.get_attribute("href")

    year = next(
        (
            int(line)
            for line in reversed(lines)
            if line.isdigit() and len(line) == 4
        ),
        None
    )

    title = album_link.get_attribute("title") or album_link.text.strip()

    if title and year:
        album_data.append({
            "title": title,
            "year": year,
            "link": href
        })

album_data.sort(key=lambda album: album["year"])

for album in album_data:
    print(album)

folder = Path("src/discographys/Babyface")
folder.mkdir(parents=True, exist_ok=True)

file_path = folder / "Babyface_disc.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(album_data, file, indent=4, ensure_ascii=False)