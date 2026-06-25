from bs4 import BeautifulSoup
import requests
import pyperclip
import re

url = "https://en.wikipedia.org/wiki/112_(band)"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
paragraphs = soup.find_all("p")
paragraph_list = [p.get_text(" ", strip=True) for p in paragraphs]
paragraph_list_strip = "\n".join(paragraph_list)
final_paragraph_list = re.sub(r"\[\s*\d+\s*\]", "", paragraph_list_strip)
final_paragraph_list = re.sub(r"\s+([,.;:!?])", "", final_paragraph_list)
#print(final_paragraph_list)
print((final_paragraph_list))
pyperclip.copy(final_paragraph_list) 

with open("112.txt", "w") as file:
    file.writelines(final_paragraph_list)