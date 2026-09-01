from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get("https://youtube.com/search?q=aaliyah+-+topic&sp=EgIQAg%253D%253D")
link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a[href^='/channel/']")
    )
)
wherewewannago = link.get_attribute("href")
print(wherewewannago)
driver.get(wherewewannago)
time.sleep(5)

driver.quit()