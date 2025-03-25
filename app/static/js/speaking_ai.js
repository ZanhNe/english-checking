const micBtn = document.querySelector(".mic-button");
const stopBtn = document.querySelector(".mic-stop");
const messages = document.querySelector(".chat-messages");

let mediaRecorder;
let chunks = [];

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (ev) => {
      chunks.push(ev.data);
      //   console.log(chunks);
    };

    mediaRecorder.onstop = (e) => {
      const blob = new Blob(chunks, { type: "audio/mp3" });
      chunks = [];
      const audioURL = URL.createObjectURL(blob);
      messages.innerHTML += `
        <div class="user-message">
            <div class="message-content">
              <audio controls>
                <source src="${audioURL}" type="audio/mpeg">
                Your browser does not support the audio element.
              </audio>
            </div>
        </div>
      `;
      const form = new FormData();
      form.append("file", blob, "record.mp3");
      fetch("http://127.0.0.1:5000/api/v1/speaking/ai/upload", {
        method: "POST",
        credentials: "include",

        body: form,
      })
        .then((res) => res.json())
        .then((res) => {
          // console.log(res);
          messages.innerHTML += `
          <div class="ai-message">
            <div class="message-content">
              <p>
                ${res.result.ai}
              </p>
            </div>
          </div>
          `;
        })
        .catch((err) => console.log(err));
    };

    mediaRecorder.start();
    console.log("Đang record");
  } catch (error) {
    console.log("Phải cho phép record mới được");
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

micBtn.addEventListener("click", () => {
  micBtn.classList.toggle("hidden");
  stopBtn.classList.toggle("hidden");
  startRecording();
});

stopBtn.addEventListener("click", () => {
  micBtn.classList.toggle("hidden");
  stopBtn.classList.toggle("hidden");
  stopRecording();
});
