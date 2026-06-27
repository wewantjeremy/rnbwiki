import requests
from bs4 import BeautifulSoup
import subprocess

def get_getty():
  url = input("Enter url: ")
  name = input("Enter name: ")
  headers = {
      "User-Agent": "Mozilla/5.0"
  }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "html.parser")
  images = soup.select('source[data-testid="asset-picture-source"]')

  for i, img in enumerate(images):
    srcset = img.get("srcset", "")
    actual_url = srcset.split(",")[-1].strip().split(" ")[0]
    subprocess.run(['curl', '-o', f"src/images/{name}_{i}.jpg", actual_url])

  print("complete")


get_getty()