document.addEventListener("DOMContentLoaded", (event) => {
  const form = document.getElementById("extractor-form");
  const resultDiv = document.getElementById("result");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const url = e.target.url.value;
    const apiURL = `https://twitter-application.onrender.com/extract_content/?url=${encodeURIComponent(
      url
    )}`;

    resultDiv.textContent = "Loading...";

    try {
      const response = await fetch(apiURL);
      const data = await response.json();

      if (data.content) {
        // "\n"を"<br>"に置換
        const formattedContent = data.content.replace(/\n/g, "<br>");

        // HTML要素にセット
        resultDiv.innerHTML = formattedContent;

        // 文字列をクリップボードにコピー
        copyToClipboard(data.content);
      } else {
        resultDiv.textContent = "No content found";
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      resultDiv.textContent = "An error occurred while fetching data";
    }
  });
});

function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(function () {
      console.log("Text successfully copied to clipboard");
    })
    .catch(function (err) {
      console.error("Unable to copy text to clipboard", err);
    });
}
