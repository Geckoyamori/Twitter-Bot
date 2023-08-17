# ローカル実行用ファイル
#
# ①サイトの記事から本文を抽出
#
# ②抽出した内容をもとにChatGPTに連投ツイートを作成してもらうためのプロンプトをoutput.txtファイルに出力


# pip3 install requests
# pip3 install beautifulsoup4
# pip3 install requests-html

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession

# URLからドメインを取得
url = "https://decrypt.co/152361/donald-trump-ethereum-crypto-holdings"
parsed_url = urlparse(url)
domain = parsed_url.netloc

# URLの中身を取得するメソッド（レンダリング前）
def fetch_url_content_before_rendering(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# URLの中身を取得するメソッド（レンダリング後）
def fetch_url_content_after_rendering(url):
    session = HTMLSession()
    response = session.get(url)
    # JavaScriptを実行してHTMLコンテンツをレンダリング
    # タイムアウト時間を20秒に設定
    response.html.render(timeout=20000)
    return response


# ファイルからプロンプト文字列を読み込む
with open("prompt.txt", "r", encoding="utf-8") as file:
    prompt = file.read()

# 本文を抽出
if domain == "decrypt.co":
    # レスポンスを取得
    soup = fetch_url_content_before_rendering(url)
    text_content = soup.find("div", class_="post-content")

    # 新規テキストファイルを作成して出力する
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        # file.write(url + "\n\n")
        file.write("\n[記事]" + "\n")

        if text_content is None:
            file.write("Error: Could not find text content.")
        else:
            paragraphs = text_content.find_all("p", recursive=False)
            for paragraph in paragraphs:
                if paragraph.parent.name != "article":
                    file.write(paragraph.get_text() + "\n")

elif domain == "www.coindesk.com":
    # レスポンスを取得
    soup = fetch_url_content_before_rendering(url)
    text_content = soup.find("div", class_="at-content-wrapper")

    # 新規テキストファイルを作成して出力する
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        # file.write(url + "\n\n")
        file.write("\n[記事]" + "\n")

        # 本文の段落要素（<p>タグ）を取得し、テキストを表示
        for paragraph in text_content.find_all("p"):
            if paragraph.text == "DISCLOSURE":
                break
            file.write(paragraph.get_text() + "\n")

elif domain == "cointelegraph.com":
    # レスポンスを取得
    soup = fetch_url_content_after_rendering(url)
    text_content = soup.html.find(".post-content", first=True)
    
    # 新規テキストファイルを作成して出力する
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        # file.write(url + "\n\n")
        file.write("\n[記事]" + "\n")

        # 本文の段落要素（<p>タグおよび<blockquote>タグ）を取得し、テキストを表示
        for paragraph in text_content.find("p, blockquote"):
            # <p>タグの1階層下に<strong>タグがある場合を除外
            if paragraph.tag == "p" and paragraph.find("strong", first=True) is not None:
                continue
            file.write(paragraph.text + "\n")



