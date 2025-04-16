async function fetchUser() {
  const res = await fetch("http://127.0.0.1:5000/api/user", {
    credentials: "include"
  });
  const box = document.getElementById("user-box");
  if (res.ok) {
    const data = await res.json();
    box.innerHTML = `Logged in as: ${data.email}`;
  } else {
    box.innerHTML = "Not logged in";
  }
}

function login() {
  window.location.href = "http://127.0.0.1:5000/api/login";
}

async function logout() {
  await fetch("http://127.0.0.1:5000/api/logout", {
    credentials: "include"
  });
  fetchUser();
}

fetchUser();
