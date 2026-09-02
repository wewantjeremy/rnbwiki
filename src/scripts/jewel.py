from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
driver.get("https://icecartel.com/products/s925-moissanite-tennis-chain-14k-gold")
link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "img[href^='//icecartel']")
    )
)
wherewewannago = link.get_attribute("href")
print(wherewewannago)
driver.get(wherewewannago)
time.sleep(5)

driver.quit()