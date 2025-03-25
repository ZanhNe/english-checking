const passwordElement = document.querySelector("#password");
const cfPasswordElement = document.querySelector("#confirm-password");
const formSubmit = document.querySelector(".form-submit");
const formContainer = document.querySelector(".form-container");
const btnSubmit = document.querySelector("#submit");

btnSubmit.addEventListener("submit", (e) => {
  e.preventDefault();
  if (passwordElement.value !== cfPasswordElement.value) {
    formContainer.innerHTML += `<p>Mật khẩu xác nhận phải trùng khớp với mật khẩu đã nhập</p>`;
    return;
  }
  btnSubmit.submit();
});
