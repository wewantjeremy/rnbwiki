from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
import json

driver = webdriver.Chrome()

driver.get(
    "https://music.youtube.com/browse/MPADUCqfo5jdnv59Ap8Ep5_Ybdgw"
)

# Find all artist/channel results
results = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (
            By.CSS_SELECTOR,
            "ytmusic-responsive-list-item-renderer"
        )
    )
)

artist_link = None

for result in results:
    lines = [
        line.strip()
        for line in result.text.split("\n")
        if line.strip()
    ]

    print(lines)



    artist_link = result.find_element(
        By.CSS_SELECTOR,
        "a[href^='channel/']"
    )


# Find the actual Albums LINK
album_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//a[.//yt-formatted-string[normalize-space()='Albums']]"
        )
    )
)

albums_url = album_link.get_attribute("href")

print("ALBUMS:", albums_url)

# ACTUALLY GO TO THE ALBUMS PAGE
driver.get(albums_url)


grid = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ytmusic-grid-renderer")
    )
)

items = grid.find_element(
    By.CSS_SELECTOR,
    "#items"
)

cards = items.find_elements(
    By.CSS_SELECTOR,
    "ytmusic-two-row-item-renderer"
)

album_links = []

for card in cards:
    link = card.find_element(
        By.CSS_SELECTOR,
        "a[href^='browse/']"
    )

    album_links.append(link)


albums = {}

for link in album_links:
    title = link.text.strip()
    href = link.get_attribute("href")

    if title:
        albums[href] = title


texts = grid.text.split("\n")

years = [
    x for x in texts
    if x.isdigit() and len(x) == 4
]

print(years)
print(grid.text.split("\n"))


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

for album in album_data:
    print(album)


folder = Path("src/discographys/Christopher Williams")
folder.mkdir(
    parents=True,
    exist_ok=True
)

file_path = folder / "Christopher Williams_disc.json"

with open(
    file_path,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        album_data,
        file,
        indent=4,
        ensure_ascii=False
    )

driver.quit()