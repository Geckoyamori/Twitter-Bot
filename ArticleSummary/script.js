// フォームの参照を取得
const form = document.getElementById("url-form");
// 結果を表示するエリアの参照を取得
const resultDiv = document.getElementById("result");

// フォームが送信されたときのイベントリスナーを設定
form.addEventListener("submit", function (event) {
  // フォームのデフォルトの送信動作を防ぐ
  event.preventDefault();

  // 入力されたURLを取得
  const url = document.getElementById("url-input").value;

  // APIのURLを構築
  const apiURL = `https://twitter-application.onrender.com/extract_content/?url=${encodeURIComponent(
    url
  )}`;

  // APIにリクエストを送る
  fetch(apiURL)
    .then((response) => response.json())
    .then((data) => {
      // 結果を表示エリアに設定
      resultDiv.textContent = JSON.stringify(data, null, 2);
    })
    .catch((error) => {
      // エラーが発生した場合、それを表示エリアに表示
      resultDiv.textContent = "エラーが発生しました: " + error;
    });
});
