async function fetchUser() {
  const res = await fetch("http://localhost:5000/api/user", {
    credentials: "include"
  });
  const box = document.getElementById("user-box");
  if (res.ok) {
    const data = await res.json();
    box.innerHTML = `Logged in as: ${data.email}`;
    toggleButtons(true);
  } else {
    box.innerHTML = "Not logged in";
    toggleButtons(false);
  }
}

function login() {
  window.location.href = "http://localhost:5000/api/login";
}

async function logout() {
  await fetch("http://localhost:5000/api/logout", {
    credentials: "include"
  });
  fetchUser();
}

function toggleButtons(isLoggedIn) {
  document.getElementById("login-btn").style.display = isLoggedIn ? "none" : "inline-block";
  document.getElementById("logout-btn").style.display = isLoggedIn ? "inline-block" : "none";
}

fetchUser();
