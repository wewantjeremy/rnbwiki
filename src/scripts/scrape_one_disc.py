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
driver.get(f"https://music.youtube.com/search?q={quote('"3T"')}")

link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a[href^='channel/']")
    )
)
print(link.get_attribute("outerHTML"))
wherewewannago = link.get_attribute("href")
#print(wherewewannago)

driver.get(wherewewannago)

link2 = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR,"ytmusic-carousel a[href^='browse/']")
    )
)


albums_header = driver.find_element(
    By.XPATH,
    "//yt-formatted-string[@role='heading' and text()='Albums']"
)

album_shelf = albums_header.find_element(
    By.XPATH,
    "./ancestor::ytmusic-carousel-shelf-renderer"
)
print(album_shelf.text)
#print(album_shelf.get_attribute("href"))
album_links = album_shelf.find_elements(
    By.CSS_SELECTOR,
    "a[href^='browse/']"
)

albums = {}


# Loop through every album link Selenium found
for link in album_links:

    # Get visible text inside the link
    # Example: "Never Say Never"
    title = link.text.strip()

    # Get the URL attribute
    # Example: https://music.youtube.com/browse/MPRE...
    href = link.get_attribute("href")

    # Only save albums that have a title
    if title:

        # Add to dictionary
        # href is the key
        # title is the value
        albums[href] = title

# Print every album title and URL
for href, title in albums.items():
    print(f'title: {title}', f'year: ', f'link: {href}')
texts = album_shelf.text.split("\n")

years = [
    x for x in texts
    if x.isdigit() and len(x) == 4
]

print(years)
album_text = album_shelf.text.split("\n")

print(album_text)

album_data = []

for (href, title), year in zip(albums.items(), years):
    album_data.append({
        "title": title,
        "year": int(year),
        "link": href
    })
album_data.sort(key=lambda album: album["year"])
for album in album_data:
    print(album)
    folder = Path(f"src/discographys/3T")

    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"3T_disc.json"
    with open (file_path, "w") as file:
        json.dump(album_data, file, indent=4)
driver.quit() 
