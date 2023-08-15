document.addEventListener("DOMContentLoaded", (event) => {
  const form = document.getElementById("extractor-form");
  const resultDiv = document.getElementById("result");
  const copyButton = document.getElementById("copy-button");
  const copyBodyButton = document.getElementById("copy-body-button");
  let formattedContent = ""; // For Clipboard
  let formattedBody = ""; // For Clipboard
  let formattedContentForHTML = ""; // For HTML Display

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const url = e.target.url.value;
    const apiURL = `https://twitter-application.onrender.com/extract_content/?url=${encodeURIComponent(
      url
    )}`;

    resultDiv.textContent = "Loading...";
    copyButton.style.display = "none"; // Initially hide the copy button
    copyBodyButton.style.display = "none"; // Initially hide the copy button

    try {
      const response = await fetch(apiURL);
      const data = await response.json();

      if (data.prompt) {
        formattedContent = data.prompt;
        formattedBody = data.body;
        formattedContentForHTML = data.prompt.replace(/\n/g, "<br>");
        resultDiv.innerHTML = formattedContentForHTML;
        copyButton.style.display = "block";
        copyBodyButton.style.display = "block";
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
  copyBodyButton.addEventListener("click", function () {
    copyToClipboard(formattedBody || "");
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
