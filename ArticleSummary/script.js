document.addEventListener("DOMContentLoaded", (event) => {
  const form = document.getElementById("extractor-form");
  const resultDiv = document.getElementById("result");
  const copyButton = document.getElementById("copy-button");
  let formattedContent = "";

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const url = e.target.url.value;
    const apiURL = `https://twitter-application.onrender.com/extract_content/?url=${encodeURIComponent(
      url
    )}`;

    resultDiv.textContent = "Loading...";
    copyButton.style.display = "none"; // Initially hide the copy button

    try {
      const response = await fetch(apiURL);
      const data = await response.json();

      if (data.content) {
        // "\n"を"<br>"に置換
        formattedContent = data.content.replace(/\n/g, "<br>");
        // HTML要素にセット
        resultDiv.innerHTML = formattedContent;
        copyButton.style.display = "block"; // Show the copy button when content is loaded
      } else {
        resultDiv.textContent = "No content found";
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      resultDiv.textContent = "An error occurred while fetching data";
    }
  });

  copyButton.addEventListener("click", function () {
    copyToClipboard(formattedContent || "");
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
