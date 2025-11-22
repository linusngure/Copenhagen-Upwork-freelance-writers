// =========================
// Login form handler
// =========================
// Let the form submit to Flask — no preventDefault here
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', () => {
    // Optional: you could add client-side validation here
    // but don't block submission
  });
}

// =========================
// Register form handler
// =========================
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', (e) => {
    const password = registerForm.password.value;
    const confirm = registerForm.confirmPassword.value;

    if (password !== confirm) {
      e.preventDefault(); // only block if invalid
      alert("Passwords do not match!");
    }
    // Otherwise, let Flask handle registration and redirect
  });
}

// =========================
// Forgot password handler
// =========================
const forgotForm = document.getElementById('forgotForm');
if (forgotForm) {
  forgotForm.addEventListener('submit', () => {
    // Let Flask handle sending reset link
  });
}

// =========================
// FAQ accordion toggle
// =========================
document.querySelectorAll('.faq-question').forEach(button => {
  button.addEventListener('click', () => {
    const item = button.parentElement;
    item.classList.toggle('active');
  });
});

// =========================
// Mobile menu toggle
// =========================
function toggleMenu() {
  const menu = document.getElementById('menu');
  if (menu) {
    menu.classList.toggle('open');
  }
}
