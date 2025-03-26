"use strict";
const checkButton = document.querySelector("#check-button");
const feedbackSection = document.querySelector(".feedback-section");
const writtingOutput = document.querySelector("#writing-input");
const loader = document.querySelector(".loader");

checkButton.addEventListener("click", function () {
  if (!writtingOutput.value.trim()) return;
  const text = writtingOutput.value;
  loader.style.display = "block";
  fetch("https://englishlearning.up.railway.app/api/v1/agent/writing", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({ text }),
  })
    .then((res) => res.json())
    .then((resJson) => {
      console.log(resJson);
      resJson.forEach(
        (value) =>
          (feedbackSection.innerHTML += `
          <div class="error-container" id="grammar-errors">
            <h4 class="error-type">Lỗi ngữ pháp</h4>
            <div id="grammar-errors-content">${value.error}</div>
          </div>

          <div class="improvement-section">
            <h4 class="improvement-title">Câu sau khi chỉnh sửa</h4>
            <div class="revised-text" id="revised-text">${value.suggestion}</div>
          </div>`)
      );
    })
    .then(() => (loader.style.display = "none"));
});
