import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

def download_google_images(max_images=10):
    driver = webdriver.Chrome()

    search = input("enter a url: ")
    driver.get(search)
    input("solve to continue")

    folder = "After 7"
    os.makedirs(folder, exist_ok=True)

    image_urls = set()
    i = 0

    while len(image_urls) < max_images:
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "img[src]")

        if i >= len(thumbnails):
            break

        try:
            img = thumbnails[i]

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                img
            )
            time.sleep(0.5)

            driver.execute_script(
                "arguments[0].click();",
                img
            )
            time.sleep(1)

            actual_images = driver.find_elements(
                By.CSS_SELECTOR,
                "img[src]"
            )

            for actual_img in actual_images:
                src = actual_img.get_attribute("src")

                if (
                    src
                    and src.startswith("http")
                    and "encrypted-tbn0.gstatic.com" not in src
                    and "instagram.com" not in src
                    and "google" not in src
                ):
                    image_urls.add(src)
                    print("found:", src)

        except Exception as e:
            print("skip:", e)

        i += 1

    driver.quit()

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, timeout=10)

            with open(f"{folder}/image_{i+1}.jpg", "wb") as f:
                f.write(response.content)

            print(f"Successfully downloaded {i+1}/{max_images}")

        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")


    
    # requests.get creates the download, 
    # "wb" means write binary which allows it to store the pic
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, timeout=10)
            with open (f"{folder}/image_{i+1}.jpg", "wb") as f:
                f.write(response.content)
            print(f"Successfully downloaded {i+1}/{max_images}")
        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")


download_google_images(5)
