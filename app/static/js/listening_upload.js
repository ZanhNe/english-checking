const submitBtn = document.querySelector("#button");
const resetBtn = document.querySelector("#button-reset");
const resultsBox = document.querySelector("#result-box");
const loader = document.querySelector(".loader");
const form = document.querySelector("form");

submitBtn.addEventListener("click", (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  if (!formData.get("file") || !formData.get("audio-upload")) return;
  loader.style.display = "block";
  fetch("https://english.up.railway.app/api/v1/listening/uploads", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
      res.results.forEach((result) => {
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

resetBtn.addEventListener("click", (e) => {
  questionArea.value = ``;
  resultsBox.innerHTML = ``;
});
