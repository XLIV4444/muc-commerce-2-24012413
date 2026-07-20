const form = document.querySelector("#question-form");
const input = document.querySelector("#question");
const answer = document.querySelector("#answer");

async function askQuestion(question) {
  answer.textContent = "正在查询项目数据……";
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();
    answer.textContent = data.answer;
  } catch (error) {
    answer.textContent = "请求失败，请确认Flask服务仍在运行。";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (question) askQuestion(question);
});

document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.question;
    askQuestion(button.dataset.question);
  });
});
