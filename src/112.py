from bs4 import BeautifulSoup
import requests
import pyperclip

url = "https://en.wikipedia.org/wiki/112_(band)"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
p = BeautifulSoup.find("div", class_="content")
soup = BeautifulSoup(response.content, "html.parser")
pyperclip.copy(p)

with open("112.txt", "w") as file:
    file.writelines(112)