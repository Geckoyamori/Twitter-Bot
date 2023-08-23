# ローカルでの実行方法

①FastAPI ベースの Web アプリケーションをローカル起動
uvicorn main:app --reload
②API を呼び出す　※URL は任意
curl -G http://127.0.0.1:8000/extract_content/ --data-urlencode "url=https://jp.cointelegraph.com/news/chinese-official-sentenced-life-prison-bitcoin-mining-corruption"

# サーバーでの実行方法

① 修正をコミット＆push する
②render に自動デプロイされる（バックエンド）
https://dashboard.render.com/web/srv-cjdfk6ivvtos73av0f4g
③Github pages に自動デプロイされる（フロントエンド）
https://github.com/Geckoyamori/Twitter-Bot/settings/pages
④web サイトから URL を入力して実行
https://geckoyamori.github.io/Twitter-Bot/ArticleSummary/
