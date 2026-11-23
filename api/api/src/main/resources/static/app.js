/* ══════════════════════════════════════════════════════════════════════
   InMemoriam — Lógica de cliente (app.js)
   Conecta con la API REST en http://localhost:8081/api/difuntos
   CRUD Completo: Crear (POST), Consultar (GET), Actualizar (PUT), Eliminar (DELETE)
   ══════════════════════════════════════════════════════════════════════ */

'use strict';

// ── Configuración ────────────────────────────────────────────────────────
const API_BASE = 'http://localhost:8081/api/difuntos';

// ── Estado global ────────────────────────────────────────────────────────
let paginaActual     = 0;
let totalPaginas     = 1;
let totalRegistros   = 0;
let pendingDeleteId  = null;
let currentDetailId  = null;
let toastTimer       = null;

// ════════════════════════════════════════════════════════════════════════
// INICIALIZACIÓN
// ════════════════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  verificarConexion();
  cargarDifuntos();

  // Enter en inputs de búsqueda y eliminación
  document.getElementById('searchId').addEventListener('keydown', e => {
    if (e.key === 'Enter') buscarPorId();
  });
  document.getElementById('deleteId').addEventListener('keydown', e => {
    if (e.key === 'Enter') confirmarEliminacion();
  });
});

// ════════════════════════════════════════════════════════════════════════
// VERIFICAR CONEXIÓN CON LA API
// ════════════════════════════════════════════════════════════════════════
async function verificarConexion() {
  const dot   = document.getElementById('statusDot');
  const label = document.getElementById('statusLabel');
  try {
    const res = await fetch(`${API_BASE}?page=0&size=1`);
    if (res.ok) {
      dot.className = 'status-dot online';
      label.textContent = 'API conectada (Puerto 8081)';
    } else {
      throw new Error('No OK');
    }
  } catch {
    dot.className = 'status-dot offline';
    label.textContent = 'API sin conexión';
  }
}

// ════════════════════════════════════════════════════════════════════════
// CARGAR LISTADO PAGINADO (GET)
// ════════════════════════════════════════════════════════════════════════
async function cargarDifuntos(pagina = 0) {
  const size = Number(document.getElementById('pageSize').value);
  paginaActual = pagina;

  mostrarSpinner(true);
  document.getElementById('tableWrap').style.display = 'none';
  document.getElementById('pagination').style.display = 'none';
  document.getElementById('emptyState').classList.add('hidden');

  try {
    const res = await fetch(`${API_BASE}?page=${pagina}&size=${size}`);
    const data = await res.json();

    if (!res.ok) {
      mostrarToast(`Error ${data.codigo}: ${data.mensaje}`, 'error');
      mostrarSpinner(false);
      return;
    }

    totalPaginas   = data.totalPaginas   ?? 1;
    totalRegistros = data.totalRegistros ?? 0;
    const difuntos = data.datos ?? [];

    if (difuntos.length === 0) {
      mostrarSpinner(false);
      document.getElementById('emptyState').classList.remove('hidden');
      renderPaginacion(data);
      document.getElementById('pagination').style.display = 'flex';
      return;
    }

    renderTabla(difuntos);
    renderPaginacion(data);

    mostrarSpinner(false);
    document.getElementById('tableWrap').style.display = 'block';
    document.getElementById('pagination').style.display = 'flex';

  } catch (err) {
    console.error('Error al cargar difuntos:', err);
    mostrarSpinner(false);
    mostrarToast('No se pudo conectar con la API. Verifique que el servidor esté en ejecución.', 'error');
    document.getElementById('emptyState').classList.remove('hidden');
  }
}

// ════════════════════════════════════════════════════════════════════════
// BUSCAR POR ID (GET)
// ════════════════════════════════════════════════════════════════════════
async function buscarPorId() {
  const id = document.getElementById('searchId').value.trim();
  if (!id) {
    mostrarToast('Ingrese un ID para buscar.', 'info');
    return;
  }
  if (Number(id) <= 0) {
    mostrarToast('El ID debe ser un número entero positivo.', 'error');
    return;
  }

  try {
    const res  = await fetch(`${API_BASE}/${id}`);
    const data = await res.json();

    if (!res.ok) {
      cerrarDetalle();
      mostrarToast(`Error ${data.codigo}: ${data.mensaje}`, 'error');
      return;
    }

    mostrarDetalle(data.datos);
    mostrarToast('Difunto encontrado correctamente.', 'success');

  } catch (err) {
    console.error('Error al buscar difunto:', err);
    mostrarToast('Error de conexión al buscar el difunto.', 'error');
  }
}

// ════════════════════════════════════════════════════════════════════════
// MODAL DE CREACIÓN / EDICIÓN (POST / PUT)
// ════════════════════════════════════════════════════════════════════════
function abrirModalCrear() {
  document.getElementById('formDifuntoId').value = '';
  document.getElementById('formModalTitle').textContent = 'Registrar Nuevo Difunto';
  document.getElementById('difuntoForm').reset();
  document.getElementById('formActivo').value = 'true';
  document.getElementById('formModalOverlay').classList.remove('hidden');
  document.getElementById('formNombre').focus();
}

async function abrirModalEditar(id) {
  try {
    mostrarToast('Cargando datos para edición...', 'info', 1500);
    const res = await fetch(`${API_BASE}/${id}`);
    const data = await res.json();

    if (!res.ok) {
      mostrarToast(`Error ${data.codigo}: ${data.mensaje}`, 'error');
      return;
    }

    const d = data.datos;
    document.getElementById('formDifuntoId').value = d.id;
    document.getElementById('formModalTitle').textContent = `Editar Difunto (ID: ${d.id})`;
    document.getElementById('formNombre').value = d.nombre || '';
    document.getElementById('formApellido').value = d.apellido || '';
    document.getElementById('formFechaNacimiento').value = d.fechaNacimiento || '';
    document.getElementById('formFechaMuerte').value = d.fechaMuerte || '';
    document.getElementById('formLugarNacimiento').value = d.lugarNacimiento || '';
    document.getElementById('formLugarMuerte').value = d.lugarMuerte || '';
    document.getElementById('formCausaMuerte').value = d.causaMuerte || '';
    document.getElementById('formEpitafio').value = d.epitafio || '';
    document.getElementById('formActivo').value = d.activo ? 'true' : 'false';

    document.getElementById('formModalOverlay').classList.remove('hidden');
    document.getElementById('formNombre').focus();

  } catch (err) {
    console.error('Error al cargar datos del difunto para editar:', err);
    mostrarToast('No se pudieron obtener los datos del difunto.', 'error');
  }
}

function cerrarModalForm() {
  document.getElementById('formModalOverlay').classList.add('hidden');
}

// ════════════════════════════════════════════════════════════════════════
// GUARDAR DIFUNTO (POST o PUT)
// ════════════════════════════════════════════════════════════════════════
async function guardarDifunto(event) {
  event.preventDefault();

  const id               = document.getElementById('formDifuntoId').value.trim();
  const nombre           = document.getElementById('formNombre').value.trim();
  const apellido         = document.getElementById('formApellido').value.trim();
  const fechaNacimiento  = document.getElementById('formFechaNacimiento').value || null;
  const fechaMuerte      = document.getElementById('formFechaMuerte').value || null;
  const lugarNacimiento  = document.getElementById('formLugarNacimiento').value.trim() || null;
  const lugarMuerte      = document.getElementById('formLugarMuerte').value.trim() || null;
  const causaMuerte      = document.getElementById('formCausaMuerte').value.trim() || null;
  const epitafio         = document.getElementById('formEpitafio').value.trim() || null;
  const activo           = document.getElementById('formActivo').value === 'true';

  if (!nombre) {
    mostrarToast('El nombre es obligatorio.', 'error');
    return;
  }
  if (!apellido) {
    mostrarToast('El apellido es obligatorio.', 'error');
    return;
  }
  if (!fechaMuerte) {
    mostrarToast('La fecha de fallecimiento es obligatoria.', 'error');
    return;
  }

  const difuntoBody = {
    nombre,
    apellido,
    fechaNacimiento,
    fechaMuerte,
    lugarNacimiento,
    lugarMuerte,
    causaMuerte,
    epitafio,
    activo
  };

  const esEdicion = Boolean(id);
  const url       = esEdicion ? `${API_BASE}/${id}` : API_BASE;
  const metodo    = esEdicion ? 'PUT' : 'POST';

  try {
    const btnGuardar = document.getElementById('btnGuardar');
    btnGuardar.disabled = true;
    btnGuardar.textContent = 'Guardando...';

    const res = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(difuntoBody)
    });

    const data = await res.json();
    btnGuardar.disabled = false;
    btnGuardar.innerHTML = '<span>&#10004;</span> Guardar';

    if (!res.ok) {
      mostrarToast(`Error ${data.codigo}: ${data.mensaje}`, 'error');
      return;
    }

    cerrarModalForm();
    mostrarToast(data.mensaje || (esEdicion ? 'Actualizado correctamente.' : 'Registrado correctamente.'), 'success');

    // Recargar tabla en la página actual (o la primera si es creación)
    await cargarDifuntos(esEdicion ? paginaActual : 0);

    // Si el panel de detalle mostraba este difunto, refrescarlo
    if (esEdicion && currentDetailId === Number(id)) {
      mostrarDetalle(data.datos);
    }

  } catch (err) {
    console.error('Error al guardar difunto:', err);
    mostrarToast('Error de conexión al intentar guardar.', 'error');
    const btnGuardar = document.getElementById('btnGuardar');
    btnGuardar.disabled = false;
    btnGuardar.innerHTML = '<span>&#10004;</span> Guardar';
  }
}

// ════════════════════════════════════════════════════════════════════════
// ACCIONES DESDE EL PANEL DE DETALLE
// ════════════════════════════════════════════════════════════════════════
function editarDesdeDetalle() {
  if (currentDetailId) {
    abrirModalEditar(currentDetailId);
  }
}

function eliminarDesdeDetalle() {
  if (currentDetailId) {
    document.getElementById('deleteId').value = currentDetailId;
    confirmarEliminacion();
  }
}

// ════════════════════════════════════════════════════════════════════════
// ELIMINAR DIFUNTO (DELETE)
// ════════════════════════════════════════════════════════════════════════
function confirmarEliminacion() {
  const id = document.getElementById('deleteId').value.trim();
  if (!id) {
    mostrarToast('Ingrese el ID del difunto a eliminar.', 'info');
    return;
  }
  if (Number(id) <= 0) {
    mostrarToast('El ID debe ser un número entero positivo.', 'error');
    return;
  }
  pendingDeleteId = id;
  document.getElementById('modalBody').innerHTML =
    `¿Está seguro de que desea eliminar el registro con <strong>ID ${id}</strong>?<br/>
     <span style="color:#e05252">Esta acción no se puede deshacer.</span>`;
  document.getElementById('modalOverlay').classList.remove('hidden');
}

function eliminarDesdeTabla(id) {
  document.getElementById('deleteId').value = id;
  confirmarEliminacion();
}

async function ejecutarEliminacion() {
  cerrarModal();
  const id = pendingDeleteId;
  if (!id) return;

  try {
    const res  = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
    const data = await res.json();

    if (!res.ok) {
      mostrarToast(`Error ${data.codigo}: ${data.mensaje}`, 'error');
      return;
    }

    mostrarToast(data.mensaje ?? `Registro ${id} eliminado correctamente.`, 'success');
    document.getElementById('deleteId').value = '';
    pendingDeleteId = null;

    if (currentDetailId === Number(id)) {
      cerrarDetalle();
    }

    await cargarDifuntos(paginaActual);

  } catch (err) {
    console.error('Error al eliminar difunto:', err);
    mostrarToast('Error de conexión al intentar eliminar el registro.', 'error');
  }
}

function cerrarModal() {
  document.getElementById('modalOverlay').classList.add('hidden');
}

// ════════════════════════════════════════════════════════════════════════
// RENDERIZAR TABLA
// ════════════════════════════════════════════════════════════════════════
function renderTabla(difuntos) {
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = '';

  difuntos.forEach(d => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong style="color:var(--accent-soft)">${d.id}</strong></td>
      <td>${esc(d.nombre)}</td>
      <td>${esc(d.apellido)}</td>
      <td>${formatFecha(d.fechaNacimiento)}</td>
      <td>${formatFecha(d.fechaMuerte)}</td>
      <td title="${esc(d.lugarNacimiento ?? '')}">${esc(d.lugarNacimiento ?? '—')}</td>
      <td title="${esc(d.lugarMuerte ?? '')}">${esc(d.lugarMuerte ?? '—')}</td>
      <td title="${esc(d.causaMuerte ?? '')}">${esc(d.causaMuerte ?? '—')}</td>
      <td class="epitafio-cell" title="${esc(d.epitafio ?? '')}">${esc(d.epitafio ?? '—')}</td>
      <td>
        <span class="badge ${d.activo ? 'badge-active' : 'badge-inactive'}">
          ${d.activo ? '● Activo' : '○ Inactivo'}
        </span>
      </td>
      <td>
        <button class="btn-icon-edit" onclick="abrirModalEditar(${d.id})" title="Editar este registro">
          &#9998; Editar
        </button>
        <button class="btn-icon-delete" onclick="eliminarDesdeTabla(${d.id})" title="Eliminar este registro">
          &#128465; Eliminar
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ════════════════════════════════════════════════════════════════════════
// RENDERIZAR PAGINACIÓN
// ════════════════════════════════════════════════════════════════════════
function renderPaginacion(data) {
  const size = Number(document.getElementById('pageSize').value);

  const inicio = totalRegistros === 0 ? 0 : paginaActual * size + 1;
  const fin    = Math.min(inicio + size - 1, totalRegistros);
  document.getElementById('pagInfo').textContent =
    totalRegistros === 0
      ? 'Sin registros'
      : `Mostrando ${inicio}–${fin} de ${totalRegistros} registros · Página ${paginaActual + 1} de ${totalPaginas}`;

  document.getElementById('btnPrimera').disabled   = paginaActual === 0;
  document.getElementById('btnAnterior').disabled  = paginaActual === 0;
  document.getElementById('btnSiguiente').disabled = paginaActual >= totalPaginas - 1;
  document.getElementById('btnUltima').disabled    = paginaActual >= totalPaginas - 1;

  const contenedor = document.getElementById('paginasBotones');
  contenedor.innerHTML = '';
  const rango = 2;
  let inicio_p = Math.max(0, paginaActual - rango);
  let fin_p    = Math.min(totalPaginas - 1, paginaActual + rango);

  if (inicio_p > 0) {
    agregarBotonPagina(contenedor, 0);
    if (inicio_p > 1) contenedor.appendChild(crearEllipsis());
  }
  for (let i = inicio_p; i <= fin_p; i++) {
    agregarBotonPagina(contenedor, i);
  }
  if (fin_p < totalPaginas - 1) {
    if (fin_p < totalPaginas - 2) contenedor.appendChild(crearEllipsis());
    agregarBotonPagina(contenedor, totalPaginas - 1);
  }
}

function agregarBotonPagina(contenedor, num) {
  const btn = document.createElement('button');
  btn.className = 'btn-pag-num' + (num === paginaActual ? ' active' : '');
  btn.textContent = num + 1;
  btn.onclick = () => irAPagina(num);
  contenedor.appendChild(btn);
}

function crearEllipsis() {
  const span = document.createElement('span');
  span.textContent = '…';
  span.style.cssText = 'color:var(--text-3);padding:0 4px;line-height:30px;';
  return span;
}

function irAPagina(num) {
  if (num < 0 || num >= totalPaginas) return;
  cargarDifuntos(num);
}

function cambiarTamano() {
  cargarDifuntos(0);
}

// ════════════════════════════════════════════════════════════════════════
// PANEL DE DETALLE
// ════════════════════════════════════════════════════════════════════════
function mostrarDetalle(d) {
  currentDetailId = d.id;
  const panel = document.getElementById('detailPanel');

  const campos = [
    { label: 'ID',              valor: d.id },
    { label: 'Nombre',          valor: d.nombre },
    { label: 'Apellido',        valor: d.apellido },
    { label: 'Fecha Nacimiento',valor: formatFecha(d.fechaNacimiento) },
    { label: 'Fecha Muerte',    valor: formatFecha(d.fechaMuerte) },
    { label: 'Lugar Nacimiento',valor: d.lugarNacimiento },
    { label: 'Lugar Muerte',    valor: d.lugarMuerte },
    { label: 'Causa Muerte',    valor: d.causaMuerte },
    { label: 'Epitafio',        valor: d.epitafio },
    { label: 'Estado',          valor: d.activo ? '● Activo' : '○ Inactivo' },
  ];

  document.getElementById('detailContent').innerHTML = `
    <div class="detail-grid">
      ${campos.map(c => `
        <div class="detail-item">
          <div class="detail-item-label">${c.label}</div>
          <div class="detail-item-value ${!c.valor ? 'muted' : ''}">
            ${c.valor != null && c.valor !== '' ? esc(String(c.valor)) : 'Sin datos'}
          </div>
        </div>
      `).join('')}
    </div>
  `;

  panel.classList.remove('hidden');
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function cerrarDetalle() {
  currentDetailId = null;
  document.getElementById('detailPanel').classList.add('hidden');
  document.getElementById('searchId').value = '';
}

// ════════════════════════════════════════════════════════════════════════
// TOAST
// ════════════════════════════════════════════════════════════════════════
function mostrarToast(mensaje, tipo = 'info', duracion = 3800) {
  const toast = document.getElementById('toast');
  toast.className = `toast ${tipo}`;
  toast.textContent = mensaje;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.add('hidden'), duracion);
}

// ════════════════════════════════════════════════════════════════════════
// HELPERS
// ════════════════════════════════════════════════════════════════════════
function mostrarSpinner(visible) {
  document.getElementById('spinner').style.display = visible ? 'flex' : 'none';
}

function formatFecha(fecha) {
  if (!fecha) return '<span style="color:var(--text-3)">—</span>';
  try {
    const [y, m, d] = String(fecha).split('-');
    return `${d}/${m}/${y}`;
  } catch {
    return esc(String(fecha));
  }
}

function esc(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
