const submitBtn = document.querySelector("#button");
const resetBtn = document.querySelector("#button-reset");
const form = document.querySelector("form");
const loader = document.querySelector(".loader");
const resultsBox = document.querySelector("#result-box");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  loader.style.display = "block";
  fetch("https://englishlearning.up.railway.app/api/v1/listening/check", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
      res.result.forEach((result) => {
        resultsBox.innerHTML += `
            <p><b>Question</b>: ${result.question.replace(/\n/g, "<br>")}</p>
            <p><b>Answer</b>: ${result.answer.replace(/\n/g, "<br>")}</p>
            <p><b>Explanation</b>: ${result.explanation
              .replace(/\n/g, "<br>")
              .replace(`'`, "<mark>")
              .replace(`'`, "</mark>")}</p>
            <br />
            `;
        loader.style.display = "none";
      });
    })
    .catch((err) => console.log(err));
});
