# ①以下サイトの記事から本文を抽出
# https://decrypt.co/
#
# ②抽出した内容をもとにChatGPTに連投ツイートを作成してもらうためのプロンプトをoutput.txtファイルに出力


# pip3 install requests
# pip3 install beautifulsoup4

import requests
from bs4 import BeautifulSoup

# ファイルから文字列を読み込む
with open("ArticleSummary/prompt.txt", "r", encoding="utf-8") as file:
    prompt = file.read()

url = "https://decrypt.co/124725/disney-cuts-metaverse-unit-company-wide-layoffs"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

text_content = soup.find("div", class_="post-content")

# 新規テキストファイルを作成して出力する
with open("ArticleSummary/output.txt", "w", encoding="utf-8") as file:
    file.write(prompt + "\n")
    file.write(url + "\n\n")
    file.write("#記事" + "\n")

    if text_content is None:
        file.write("Error: Could not find text content.")
    else:
        paragraphs = text_content.find_all("p", recursive=False)
        for paragraph in paragraphs:
            if paragraph.parent.name != "article":
                file.write(paragraph.get_text() + "\n")