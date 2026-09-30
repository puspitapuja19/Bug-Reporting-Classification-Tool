const form = document.getElementById("bug-form");
const spinner = document.getElementById("spinner");
const button = document.getElementById("predict-btn");

form.addEventListener("submit", () => {
  spinner.style.display = "inline-block";
  button.disabled = true;
});