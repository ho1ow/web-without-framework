document.addEventListener("DOMContentLoaded", function () {
  const registerButton = document.querySelector(".register button");
  registerButton.addEventListener("click", register);
});

function register() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document
    .getElementById("confirm_password")
    .value.trim();

  if (password !== confirmPassword) {
    alert("Passwords do not match.");
    return;
  }
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  })
    .then((response) =>
      response.json().then((data) => ({ status: response.status, body: data }))
    )
    .then(({ status, body }) => {
      if (status !== 201) {
        alert("Registration failed: " + body.message);
      } else {
        console.log("User added:", body);
        window.location.href = "/login";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Registration failed: " + error.message);
    });
}
