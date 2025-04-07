"use strict";
const checkButton = document.querySelector("#check-button-detail");
const checkGeneralBtn = document.querySelector("#check-button-general");

const feedbackSection = document.querySelector(".feedback-section");
const writtingOutput = document.querySelector("#writing-input");
const resetBtn = document.querySelector("#reset-button");
const loader = document.querySelector(".loader");

function highlightErrors(original, corrected) {
  let diff = Diff.diffWords(original, corrected); // So sánh từng từ hoặc cụm từ
  let resultHTML = "";

  diff.forEach((part) => {
    if (part.removed) {
      resultHTML += `<span class="error">${part.value}</span> `;
    } else if (!part.added) {
      resultHTML += part.value + " ";
    }
  });

  return resultHTML;
}

checkButton.addEventListener("click", function () {
  if (!writtingOutput.value.trim()) return;
  feedbackSection.innerHTML = ``;
  const text = writtingOutput.value;
  loader.style.display = "block";
  fetch("https://english.up.railway.app/api/v1/agent/writing", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({ text }),
  })
    .then((res) => res.json())
    .then((resJson) => {
      console.log(resJson);
      if (!resJson.is_correct) {
        const highlightHTML = highlightErrors(
          writtingOutput.value,
          resJson.correct_sentence
        );
        feedbackSection.innerHTML += `
         <div class="error-container" id="grammar-errors">
            <h4 class="error-type">Câu gốc</h4>
            <div id="grammar-errors-content">${highlightHTML}</div>
          </div>
        `;
        resJson.grammar_check_details.forEach((detail) => {
          feedbackSection.innerHTML += `
          <div class="error-container" id="grammar-errors">
            <h4 class="error-type">Lỗi ngữ pháp</h4>
            <div id="grammar-errors-content">${detail.error}</div>
          </div>

          <div class="improvement-section">
            <h4 class="improvement-title">Cần chỉnh sửa</h4>
            <div class="revised-text" id="revised-text">${detail.suggestion}</div>
          </div>`;
        });
        feedbackSection.innerHTML += `
          <div class="improvement-section">
            <h4 class="improvement-title">Câu sau khi chỉnh sửa</h4>
            <div class="revised-text" id="revised-text">${resJson.correct_sentence}</div>
          </div>
        `;
      } else {
        feedbackSection.innerHTML += `
          <div class="improvement-section">
            <h4 class="improvement-title">Kết quả</h4>
            <div class="revised-text" id="revised-text">Không có sai sót nào trong đoạn văn trên.</div>
          </div>;
          `;
      }
    })
    .then(() => (loader.style.display = "none"));
});

checkGeneralBtn.addEventListener("click", (e) => {
  if (!writtingOutput.value.trim()) return;
  feedbackSection.innerHTML = ``;
  const text = writtingOutput.value;
  loader.style.display = "block";

  fetch("https://english.up.railway.app/api/v1/writing/general-check", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({ text }),
  })
    .then((res) => res.json())
    .then((resJson) => {
      console.log(resJson);
      if (!resJson.is_correct) {
        const highlightHTML = highlightErrors(
          writtingOutput.value,
          resJson.correct_sentence
        );
        feedbackSection.innerHTML += `
         <div class="error-container" id="grammar-errors">
            <h4 class="error-type">Câu gốc</h4>
            <div id="grammar-errors-content">${highlightHTML}</div>
          </div>
        `;
        resJson.grammar_check_details.forEach((detail) => {
          feedbackSection.innerHTML += `
          <div class="error-container" id="grammar-errors">
            <h4 class="error-type">Lỗi ngữ pháp</h4>
            <div id="grammar-errors-content">${detail.error}</div>
          </div>

          <div class="improvement-section">
            <h4 class="improvement-title">Cần chỉnh sửa</h4>
            <div class="revised-text" id="revised-text">${detail.suggestion}</div>
          </div>`;
        });
        feedbackSection.innerHTML += `
          <div class="improvement-section">
            <h4 class="improvement-title">Câu sau khi chỉnh sửa</h4>
            <div class="revised-text" id="revised-text">${resJson.correct_sentence}</div>
          </div>
        `;
      } else {
        feedbackSection.innerHTML += `
          <div class="improvement-section">
            <h4 class="improvement-title">Kết quả</h4>
            <div class="revised-text" id="revised-text">Không có sai sót nào trong đoạn văn trên.</div>
          </div>;
          `;
      }
      loader.style.display = "none";
    })
    .catch((err) => {
      console.log(err);
    });
});

resetBtn.addEventListener("click", (e) => {
  feedbackSection.innerHTML = ``;
  writtingOutput.value = ``;
});
