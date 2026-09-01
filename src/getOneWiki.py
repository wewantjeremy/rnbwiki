import pyperclip
import re
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

here = Path(__file__).parent

bios_folder = here / "bios" / "1 of The Girls"
bios_folder.mkdir(parents=True, exist_ok=True)

file_path = bios_folder / "1 of The Girls.txt"

url = "https://en.wikipedia.org/wiki/1_of_the_Girls"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

content = soup.find("div", id="mw-content-text")
paragraphs = content.find_all("p")

text = "\n".join(
    p.get_text(" ", strip=True) for p in paragraphs if p.get_text(" ", strip=True)
)

# \s* = 1 or more spaces \d+ is 1 or more integers
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
# if there's more than 3 newlines replace it with 1
text = re.sub(r"\n{3,}", "\n", text)

print(text)
pyperclip.copy(text)

with open(file_path, "w", encoding="utf-8") as file:
    file.write(text)
