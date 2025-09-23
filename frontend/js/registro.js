// frontend/js/registro.js
(() => {
  const form = document.getElementById("registerForm");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    const password = document.getElementById("password");
    const password2 = document.getElementById("password2");

    // Validar contraseñas iguales
    if (password.value !== password2.value) {
      e.preventDefault();
      e.stopPropagation();
      password2.setCustomValidity("Las contraseñas no coinciden");
    } else {
      password2.setCustomValidity("");
    }

    if (!form.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }

    form.classList.add("was-validated");
  });
})();
