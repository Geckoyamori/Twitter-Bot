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
      console.log(response);
      const data = await response.json();
      console.log(data);
      console.log(data.content);

      if (data.content) {
        resultDiv.textContent = data.content;
      } else {
        resultDiv.textContent = "No content found";
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      resultDiv.textContent = "An error occurred while fetching data";
    }
  });
});
