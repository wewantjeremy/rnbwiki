import pyperclip
import re
import requests
from bs4 import BeautifulSoup
import json
import os
from pathlib import Path


artist = input("enter a name: ")
link = input("enter a link :")  
here = Path(__file__).parent

with open(here / "../artists.json") as f:
    artists = json.load(f)

    def scrapeBio(url, name):
        
        folder = f"src/bios/{name}"
        os.makedirs(folder, exist_ok=True)
        

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        content = soup.find("div", id="mw-content-text")
        paragraphs = content.find_all("p")

        text = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if p.get_text(" ", strip=True)
        )
        text = re.sub(r"\[\s*\d+\s*\]", "", text)

        # (x) means x = \1, or the first captured class
        # [x] means find x
        # its like 'find a space with punctuation after and replace it with just the punctuation'
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)

        # \s* = find 0 or more spaces (.*?)\s* = find 0 or more characters until the next 0 or more spaces \1 = replace with the 0 or more characters
        # note this IS HAPPENING BETWEEN QUOTATIONS
        text = re.sub(r'"\s*(.*?)\s*"', r'"\1"', text)

        # space, apostrophe is replaced by apostrophe
        text = re.sub(r"\s+'\s*", "'", text)

        # if theres more than 1 tab or space, replace it with 1 space
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n", text)
        text = re.sub(r"([(\[])\s+", r"\1", text)
        text = re.sub(r"\s+([,.;:!?)\]])", r"\1", text)
        file_path = Path(folder) / f"{name}.txt"
        paragraphs  = [p.strip() for p in text.split("\n") if p.strip()]
        if paragraphs:
            text = paragraphs[0]+ "\n" + "\n".join(
                "\t" + p for p in paragraphs[1:])

    
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
        

    scrapeBio(link, artist)


