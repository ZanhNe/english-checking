const quizForm = document.querySelector("#quiz-form");
const resetReading = document.querySelector("#reset-reading");

quizForm.addEventListener("click", (e) => {
  if (e.target.nodeName.toLowerCase() === "input") {
    console.log(e.target.name, e.target.value);
    const obj = { question: e.target.name, answer: e.target.value };
    fetch("http://127.0.0.1:5000/api/v1/reading/answer-choose", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(obj),
    })
      .then(() => console.log("Lưu thành công đáp án"))
      .catch((err) => console.log(err));
  }
});

resetReading.addEventListener("click", (e) => {
  e.preventDefault();
  fetch("http://127.0.0.1:5000/api/v1/reading/reset", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((res) => console.log(res))
    .then(() => {
      location.reload();
    })
    .catch((err) => console.log(err));
});
