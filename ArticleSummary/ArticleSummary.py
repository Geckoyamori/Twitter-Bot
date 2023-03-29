# ①以下サイトの記事から本文を抽出
# https://decrypt.co/
#
# ②抽出した内容をもとにChatGPTに連投ツイートを作成してもらうためのプロンプトをoutput.txtファイルに出力


# pip3 install requests
# pip3 install beautifulsoup4

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ファイルからプロンプト文字列を読み込む
with open("ArticleSummary/prompt.txt", "r", encoding="utf-8") as file:
    prompt = file.read()

# URLのレスポンスを取得
url = "https://decrypt.co/124779/f1-team-crypto-sponsor-kraken-after-ftx-tezos-exits"
parsed_url = urlparse(url)
domain = parsed_url.netloc
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# レスポンスから本文を抽出
if domain == "decrypt.co":
    
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

elif domain == "www.coindesk.com":
    print('a')