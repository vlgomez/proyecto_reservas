// frontend/js/login.js
(() => {
  const form = document.getElementById("loginForm");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    // Forzar validación nativa de HTML5
    if (!form.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    form.classList.add("was-validated");
  });
})();
