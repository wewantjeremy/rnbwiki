from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

driver.get("https://music.youtube.com/search?q=brandy")

# get artist channel
channel = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a[href^='channel/']")
    )
)

url = channel.get_attribute("href")

if url.startswith("/"):
    url = "https://music.youtube.com" + url

driver.get(url)

print("ON PAGE:", driver.current_url)

# find Albums heading
albums_header = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.XPATH, "//yt-formatted-string[@role='heading' and text()='Albums']")
    )
)

print("FOUND ALBUMS")

# go up to the carousel
album_shelf = albums_header.find_element(
    By.XPATH,
    "./ancestor::ytmusic-carousel-shelf-renderer"
)

albums = album_shelf.find_elements(
    By.CSS_SELECTOR,
    "a[href^='browse/']"
)

seen = {}
for album in albums:
    href = album.get_attribute("href")
    text = album.get_attribute("title")

    if not text:
        text = album.find_element(
            By.CSS_SELECTOR,
            "yt-formatted-string"
        ).text.strip()
    if href not in seen:
        seen[href] = text  # first occurrence wins

for href, text in seen.items():
    print(text)
    print(href)
print("COUNT:", len(albums))

driver.quit()