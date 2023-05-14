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
url = "https://decrypt.co/139961/ethereum-network-suffers-finality-issues-heres-what-that-means"
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

# ローカルのhtmlの中身を取得するメソッド（レンダリング後）
def fetch_html_content_after_rendering(url):
    soup = BeautifulSoup(open('ArticleSummary/input.html'), 'html.parser')
    return soup


# ファイルからプロンプト文字列を読み込む
with open("ArticleSummary/prompt.txt", "r", encoding="utf-8") as file:
    prompt = file.read()

# 本文を抽出
if domain == "decrypt.co":
    # レスポンスを取得
    soup = fetch_url_content_before_rendering(url)
    text_content = soup.find("div", class_="post-content")

    # 新規テキストファイルを作成して出力する
    with open("ArticleSummary/output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        file.write(url + "\n\n")
        file.write("[記事]" + "\n")

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
    with open("ArticleSummary/output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        file.write(url + "\n\n")
        file.write("[記事]" + "\n")

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
    with open("ArticleSummary/output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        file.write(url + "\n\n")
        file.write("[記事]" + "\n")

        # 本文の段落要素（<p>タグおよび<blockquote>タグ）を取得し、テキストを表示
        for paragraph in text_content.find("p, blockquote"):
            # <p>タグの1階層下に<strong>タグがある場合を除外
            if paragraph.tag == "p" and paragraph.find("strong", first=True) is not None:
                continue
            file.write(paragraph.text + "\n")

elif domain == "dappradar.com":
    # レスポンスを取得
    # dappradar.comはスクレイピングできない（アクセス制限がかかっている）ため、開発者コンソールからhtmlの内容を"entry-content"でgrepかけ、該当箇所をコピーして、input.htmlに貼り付けた上で実行する
    soup = fetch_html_content_after_rendering(url)
    text_content = soup.find("div", class_="entry-content")
    
    # 新規テキストファイルを作成して出力する
    with open("ArticleSummary/output.txt", "w", encoding="utf-8") as file:
        file.write(prompt + "\n")
        file.write(url + "\n\n")
        file.write("[記事]" + "\n")

        # 本文の段落要素を取得し、テキストを表示
        paragraphs = text_content.find_all(["p", "h2", "h3", "ul"], recursive=True)
        for paragraph in paragraphs:
            # 箇条書きの箇所も取得
            if paragraph.name == "ul":
                list_items = paragraph.find_all("li")
                for item in list_items:
                    file.write("- " + item.get_text() + "\n")
            else:
                file.write(paragraph.get_text() + "\n")


