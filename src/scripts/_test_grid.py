from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# MANUALLY paste the correct Babyface YouTube Music artist URL here
artist_url = "https://music.youtube.com/@McKnightOhana"

driver.get(artist_url)

# Find the Albums link on the artist page
album_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//yt-formatted-string[@role='heading']//a[normalize-space()='Albums']"
        )
    )
)

albums_url = album_link.get_attribute("href")

print("ALBUMS URL:")
print(albums_url)

driver.get(albums_url)

# Find the grid
grid = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ytmusic-grid-renderer")
    )
)

# Find album cards
cards = grid.find_elements(
    By.CSS_SELECTOR,
    "ytmusic-two-row-item-renderer"
)

print("NUMBER OF CARDS:", len(cards))
print()

for card in cards:
    print("CARD:")
    print(card.text)
    print("------")

driver.quit()