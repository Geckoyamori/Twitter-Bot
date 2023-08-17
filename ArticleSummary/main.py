# サーバー実行用ファイル
#
# ①サイトの記事から本文を抽出
#
# ②抽出した内容をもとにChatGPTに連投ツイートを作成してもらうためのプロンプトをoutput.txtファイルに出力


# pip3 install requests
# pip3 install beautifulsoup4
# pip3 install requests-html

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession
import asyncio
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "https://geckoyamori.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLの中身を取得するメソッド（レンダリング前）
def fetch_url_content_before_rendering(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# URLの中身を取得するメソッド（レンダリング後）
async def async_fetch_url_content_after_rendering(url):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(executor, fetch_url_content_after_rendering, url)
    return response

def fetch_url_content_after_rendering(url):
    session = HTMLSession()
    response = session.get(url)
    # JavaScriptを実行してHTMLコンテンツをレンダリング
    # タイムアウト時間を20秒に設定
    response.html.render(timeout=20000)
    return response

@app.get("/extract_content/")
async def extract_content_from_url(url: Optional[str] = Query(..., description="URL to extract content from")):
    # URLからドメインを取得
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # ファイルからプロンプト文字列を読み込む
    with open("prompt.txt", "r", encoding="utf-8") as file:
        prompt = file.read()

    # 本文を抽出
    if domain == "decrypt.co":
        # レスポンスを取得
        soup = fetch_url_content_before_rendering(url)
        text_content = soup.find("div", class_="post-content")

        # ChatGPTに投げるプロンプトファイルを作成する
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
        
        # 記事の本文だけを抽出するbodyファイルを作成する
        with open("body.txt", "w", encoding="utf-8") as file:
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

        # ChatGPTに投げるプロンプトファイルを作成する
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(prompt + "\n")
            # file.write(url + "\n\n")
            file.write("\n[記事]" + "\n")

            # 本文の段落要素（<p>タグ）を取得し、テキストを表示
            for paragraph in text_content.find_all("p"):
                if paragraph.text == "DISCLOSURE":
                    break
                file.write(paragraph.get_text() + "\n")

        # 記事の本文だけを抽出するbodyファイルを作成する
        with open("body.txt", "w", encoding="utf-8") as file:
            # 本文の段落要素（<p>タグ）を取得し、テキストを表示
            for paragraph in text_content.find_all("p"):
                if paragraph.text == "DISCLOSURE":
                    break
                file.write(paragraph.get_text() + "\n")

    elif domain == "cointelegraph.com":
        # レスポンスを取得
        soup = await async_fetch_url_content_after_rendering(url)
        text_content = soup.html.find(".post-content", first=True)
        
        # ChatGPTに投げるプロンプトファイルを作成する
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
        
        # 記事の本文だけを抽出するbodyファイルを作成する
        with open("body.txt", "w", encoding="utf-8") as file:
            # 本文の段落要素（<p>タグおよび<blockquote>タグ）を取得し、テキストを表示
            for paragraph in text_content.find("p, blockquote"):
                # <p>タグの1階層下に<strong>タグがある場合を除外
                if paragraph.tag == "p" and paragraph.find("strong", first=True) is not None:
                    continue
                file.write(paragraph.text + "\n")

    # 最後にoutput.txtの内容とbody.txtの内容を返す
    output = ""
    body = ""
    quote = "元記事はこちら\n"+url
    with open("output.txt", "r", encoding="utf-8") as file:
        output = file.read()

    with open("body.txt", "r", encoding="utf-8") as file:
        body = file.read()

    return {"prompt": output, "body": body, "quote": quote}

