// frontend/js/catalogo.js
async function cargarEventos() {
  const contenedor = document.getElementById("lista-eventos");
  if (!contenedor) return;
  contenedor.innerHTML = "<p class='text-muted'>Cargando eventos...</p>";

  try {
    const res = await fetch("/api/eventos");
    const eventos = await res.json();
    if (!Array.isArray(eventos) || eventos.length === 0) {
      contenedor.innerHTML = "<p class='text-muted'>No hay eventos disponibles.</p>";
      return;
    }

    contenedor.innerHTML = "";
    for (const ev of eventos) {
      const card = document.createElement("div");
      card.className = "card mb-3";

      card.innerHTML = `
        <div class="card-body">
          <h5 class="card-title">${ev.titulo}</h5>
          <p class="card-text mb-1"><strong>Fecha:</strong> ${ev.fecha_hora.replace(" ", " · ")}</p>
          <p class="card-text mb-1"><strong>Lugar:</strong> ${ev.lugar}</p>
          <p class="card-text">${ev.descripcion ?? ""}</p>
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">Disponibles: ${ev.entradas_disponibles}/${ev.aforo}</small>
            <button class="btn btn-primary btn-sm" disabled>Reservar</button>
          </div>
        </div>
      `;
      contenedor.appendChild(card);
    }
  } catch (e) {
    contenedor.innerHTML = "<p class='text-danger'>Error cargando eventos.</p>";
    console.error(e);
  }
}

document.addEventListener("DOMContentLoaded", cargarEventos);
