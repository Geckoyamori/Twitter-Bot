# Python run at the following sites
# https://replit.com/@Geckoyamori/ImpassionedDarkorangeInstructionset#main.py
#
# Function to extract only the text of the following articles, excluding advertisements and images
# https://decrypt.co/


import requests
from bs4 import BeautifulSoup

url = "https://decrypt.co/123906/openai-gpt-text-custom-metaverse-worlds"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

text_content = soup.find("div", class_="post-content")

if text_content is None:
    print("Error: Could not find text content.")
else:
    paragraphs = text_content.find_all("p", recursive=False)
    for paragraph in paragraphs:
        if paragraph.parent.name != "article":
            print(paragraph.get_text())