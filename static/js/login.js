document.addEventListener("DOMContentLoaded", function () {
  const loginButton = document.querySelector(".login button");
  loginButton.addEventListener("click", login);
});

function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  fetch("/login", {
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
      if (status !== 302) {
        alert("Login failed");
      } else {
        console.log("User login:", body);
        window.location.href = "/tasks";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Registration failed: " + error.message);
    });
}
