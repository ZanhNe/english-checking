const passageArea = document.querySelector("#passage");
const questionArea = document.querySelector("#questions");
const submitBtn = document.querySelector("#button");
const resetBtn = document.querySelector("#button-reset");
const resultsBox = document.querySelector("#result-box");
const loader = document.querySelector(".loader");

submitBtn.addEventListener("click", (e) => {
  e.preventDefault();
  const passageValue = passageArea.value;
  const questionsValue = questionArea.value;
  console.log(loader);
  const obj = {
    passage: passageValue,
    questions: questionsValue,
  };
  console.log(obj);

  if (!passageValue.trim() || !questionsValue.trim()) return;
  loader.style.display = "block";
  fetch("https://englishlearning.up.railway.app/api/v1/reading/check", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(obj),
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
              .replace(`'`, "</mark>")
              .replace('"', "<mark>")
              .replace('"', "</mark>")}</p>
            <p><b>Segment</b>: ${result.segments}</p>
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
