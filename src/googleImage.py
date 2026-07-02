import os
import time
import requests
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def screenshot_google_images(max_images=5, folder="src/images/Brownstone"):
    saved = 0
    os.makedirs(folder, exist_ok=True)

    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)

    search = input("Enter Google Images search URL: ")
    driver.get(search)

    print("Press Enter when the page is loaded...")
    input()

    time.sleep(2)

    collected_urls = set()
    image_urls = []

    try:
        print("Scrolling to load more images...")
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)

        print("Searching for image thumbnails...")

        # Target the actual search result image containers (not UI chrome)
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")

        print(f"Found {len(thumbnails)} thumbnail candidates")

        for img in thumbnails:
            if len(image_urls) >= max_images:
                break

            # Try multiple src attributes in priority order
            src = (
                img.get_attribute("src")
                or img.get_attribute("data-src")
                or img.get_attribute("data-iurl")
            )

            if not src:
                continue

            # Skip tiny UI icons (under 1KB as base64 or very short URLs)
            if src.startswith("data:image"):
                # Decode and check size
                try:
                    header, b64data = src.split(",", 1)
                    byte_len = len(base64.b64decode(b64data))
                    if byte_len < 2000:  # skip tiny icons
                        continue
                except Exception:
                    continue
            elif src in collected_urls:
                continue
            elif "google.com/images/nav" in src or "gstatic.com/images/icons" in src:
                continue

            collected_urls.add(src)
            image_urls.append(src)
            print(f"  Queued: {src[:80]}")

    except Exception as e:
        print(f"Error finding images: {e}")
        driver.quit()
        return

    driver.quit()

    print(f"\nDownloading {len(image_urls)} images...")

    for count, url in enumerate(image_urls, start=1):
        filename = f"Brownstone_{count}.jpg"
        file_path = os.path.join(folder, filename)

        try:
            if url.startswith("data:image"):
                # Save base64-encoded image directly
                header, b64data = url.split(",", 1)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(b64data))
                saved += 1
                print(f"Saved (base64) {filename}")
            else:
                response = requests.get(url, stream=True, timeout=10,
                                        headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                saved += 1
                print(f"Saved {filename}")

        except Exception as e:
            print(f"Failed on image {count}: {e}")

    print("-" * 30)
    print(f"Done. Saved {saved} images to '{folder}'")


screenshot_google_images(max_images=5)