# Import Selenium's browser control tools
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pathlib import Path
import json

here = Path(__file__).parent

with open(here / "../artists.json") as f:
    artists = json.load(f)
driver = webdriver.Chrome()
for artist in artists[40:]:
    artist_name = artist["name"]
    driver.get(f"https://music.youtube.com/search?q={artist_name}")

    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href^='channel/']")
        )
    )
    print(link.get_attribute("outerHTML"))
    wherewewannago = link.get_attribute("href")
    #print(wherewewannago)

    driver.get(wherewewannago)
    try:
        album_heading = driver.find_element(
            By.XPATH, 
            "//yt-formatted-string[@role='heading'][.//a[text()='Albums']]"
        )
        album_heading.get_attribute("href")
    except:
        album_heading = driver.find_element(
                By.XPATH, 
                "//yt-formatted-string[@role='heading' and text()='Albums']"
        )
        album_heading.get_attribute("href")
    grid = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ytmusic-grid-renderer")
        )
    )
    items = grid.find_element(By.CSS_SELECTOR, "#items")
    cards = items.find_elements(
      By.CSS_SELECTOR, "ytmusic-two-row-item-renderer"
    )
    album_links = []
for card in cards:
    link = card.find_element(
        By.CSS_SELECTOR,
        "a[href^='browse/']"
    )

    album_links.append(link)

albums = {}

# Get title + URL from each album link
for link in album_links:
    title = link.text.strip()
    href = link.get_attribute("href")

    if title:
        albums[href] = title

# Get years from the grid
texts = grid.text.split("\n")

years = [
    x for x in texts
    if x.isdigit() and len(x) == 4
]

print(years)

album_text = grid.text.split("\n")

print(album_text)

album_data = []

# Match album with year
for (href, title), year in zip(
    albums.items(),
    years
):
    album_data.append({
        "title": title,
        "year": int(year),
        "link": href
    })

# Oldest → newest
album_data.sort(
    key=lambda album: album["year"]
)

for album in album_data:
    print(album)

# Save JSON
folder = Path(
    f"src/discographys/{artist_name}"
)

folder.mkdir(
    parents=True,
    exist_ok=True
)

file_path = (
    folder /
    f"{artist_name}_disc.json"
)

with open(file_path, "w") as file:
    json.dump(
        album_data,
        file,
        indent=4
    )


driver.quit()