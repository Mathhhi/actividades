import os
import re
from functools import wraps
from io import BytesIO

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from database.conexion import obtener_conexion


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-super-secreta-cambiar-en-produccion")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_PRODUCT_PRICE = 50_000_000
PRODUCT_CODE_PATTERN = re.compile(r"^P\d{3}$")


def formatear_precios(productos):
    for producto in productos:
        try:
            producto["precio_formateado"] = f"$ {float(producto['precio']):,.2f}"
        except (ValueError, TypeError, KeyError):
            producto["precio_formateado"] = "$ 0.00"
    return productos


def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM productos ORDER BY codigo")
        return formatear_precios(cursor.fetchall())
    finally:
        cursor.close()
        conexion.close()


def usuario_actual():
    return session.get("usuario")


def requiere_login(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        if not usuario_actual():
            flash("Debes iniciar sesión para continuar.", "error")
            return redirect(url_for("login", next=request.path))
        return funcion(*args, **kwargs)

    return envoltura


def requiere_rol(rol):
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            usuario = usuario_actual()
            if not usuario:
                flash("Debes iniciar sesión para continuar.", "error")
                return redirect(url_for("login", next=request.path))
            if usuario["rol"] != rol:
                flash("No tienes permisos para acceder a esta sección.", "error")
                return redirect(url_for("inicio"))
            return funcion(*args, **kwargs)

        return envoltura

    return decorador


def validar_producto(codigo, nombre, precio, categoria, imagen=None, imagen_obligatoria=False):
    codigo = (codigo or "").strip().upper()
    nombre = " ".join((nombre or "").split())
    categoria = " ".join((categoria or "").split())
    errores = []

    if not codigo or not nombre or not categoria or precio is None or str(precio).strip() == "":
        errores.append("Todos los campos son obligatorios.")
    if codigo and not PRODUCT_CODE_PATTERN.fullmatch(codigo):
        errores.append("El código debe tener el formato P001, P002, P003.")
    if nombre and len(nombre) < 5:
        errores.append("El nombre debe tener mínimo 5 caracteres.")
    if len(nombre) > 100:
        errores.append("El nombre no puede superar 100 caracteres.")
    if categoria and any(char.isdigit() for char in categoria):
        errores.append("La categoría no puede contener números.")

    precio_val = None
    try:
        precio_val = float(precio)
        if precio_val <= 0:
            errores.append("El precio debe ser mayor que cero.")
        elif precio_val > MAX_PRODUCT_PRICE:
            errores.append("El precio no puede superar $50.000.000.")
    except (TypeError, ValueError):
        if precio is not None and str(precio).strip():
            errores.append("El precio debe ser un número válido.")

    if imagen_obligatoria and not imagen:
        errores.append("Debes seleccionar una imagen para el producto.")

    return errores, {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio_val,
        "categoria": categoria,
        "imagen": imagen,
    }


def extension_permitida(nombre):
    return "." in nombre and nombre.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def guardar_imagen(archivo):
    if not archivo or not archivo.filename:
        return None, "Debes seleccionar una imagen para el producto."
    if not extension_permitida(archivo.filename):
        return None, "La imagen debe ser PNG, JPG, JPEG o WEBP."
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    nombre_seguro = secure_filename(archivo.filename)
    nombre_final = f"{os.urandom(8).hex()}_{nombre_seguro}"
    archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_final))
    return nombre_final, None


def url_imagen_producto(nombre):
    return url_for("static", filename=f"uploads/{nombre}") if nombre != "default-product.svg" else url_for("static", filename="default-product.svg")


@app.context_processor
def datos_globales():
    return {"usuario_sesion": usuario_actual(), "url_imagen_producto": url_imagen_producto}


@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("index1.html", productos_destacados=obtener_productos())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, nombre, correo, contrasena, rol FROM usuarios WHERE correo = %s AND estado = 'activo'", (correo,))
            usuario = cursor.fetchone()
        finally:
            cursor.close()
            conexion.close()
        if usuario and check_password_hash(usuario["contrasena"], contrasena):
            session["usuario"] = {
                "id": usuario["id"],
                "nombre": usuario["nombre"],
                "correo": usuario["correo"],
                "rol": usuario["rol"],
            }
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("productos" if usuario["rol"] == "administrador" else "cliente"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html")


@app.route("/registro_usuario", methods=["GET", "POST"])
def registro_usuario():
    if request.method == "POST":
        nombre = " ".join(request.form.get("nombre", "").split())
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")
        errores = []
        if not nombre or not correo or not contrasena:
            errores.append("Todos los campos son obligatorios.")
        if correo and ("@" not in correo or "." not in correo):
            errores.append("El correo no tiene un formato válido.")
        if len(contrasena) < 8:
            errores.append("La contraseña debe tener mínimo 8 caracteres.")
        if errores:
            return render_template("registro_usuario.html", errores=errores, nombre=nombre, correo=correo)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol, estado) VALUES (%s, %s, %s, 'cliente', 'activo')",
                (nombre, correo, generate_password_hash(contrasena)),
            )
            conexion.commit()
        except Exception:
            conexion.rollback()
            flash("El correo ya está registrado o no se pudo crear la cuenta.", "error")
            return render_template("registro_usuario.html", nombre=nombre, correo=correo)
        finally:
            cursor.close()
            conexion.close()
        flash("Registro exitoso. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("login"))
    return render_template("registro_usuario.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("inicio"))


@app.route("/cliente", methods=["GET", "POST"])
@requiere_rol("cliente")
def cliente():
    usuario = usuario_actual()
    if request.method == "POST":
        nombre = " ".join(request.form.get("nombre", "").split())
        correo = request.form.get("correo", "").strip().lower()
        if not nombre or not correo or "@" not in correo:
            flash("El nombre y el correo son obligatorios y deben ser válidos.", "error")
            return render_template("dashboard_cliente.html", usuario=usuario)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s WHERE id = %s", (nombre, correo, usuario["id"]))
            conexion.commit()
            session["usuario"].update({"nombre": nombre, "correo": correo})
            flash("Tus datos fueron actualizados correctamente.", "success")
        except Exception:
            conexion.rollback()
            flash("No se pudieron actualizar tus datos.", "error")
        finally:
            cursor.close()
            conexion.close()
    return render_template("dashboard_cliente.html", usuario=session["usuario"])


@app.route("/productos")
@requiere_rol("administrador")
def productos():
    return render_template("productos.html", productos=obtener_productos())


@app.route("/admin")
@requiere_rol("administrador")
def admin():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre, correo, rol, estado FROM usuarios ORDER BY id")
        usuarios = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
    return render_template("admin.html", usuarios=usuarios, productos=obtener_productos())


@app.route("/productos/pdf")
@requiere_rol("administrador")
def productos_pdf():
    buffer = BytesIO()
    documento = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    estilos = getSampleStyleSheet()
    elementos = [Paragraph("TechStore - Listado de productos", estilos["Title"]), Spacer(1, 0.2 * inch)]
    filas = [["Código", "Nombre", "Precio", "Categoría"]]
    for producto in obtener_productos():
        filas.append([producto["codigo"], producto["nombre"], producto["precio_formateado"], producto["categoria"]])
    tabla = Table(filas, colWidths=[0.9 * inch, 2.5 * inch, 1.3 * inch, 1.7 * inch])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#212529")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabla)
    documento.build(elementos)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="productos_techstore.pdf", mimetype="application/pdf")


@app.route("/registro_producto")
@requiere_rol("administrador")
def registro_producto():
    return render_template("registro_producto.html")


@app.route("/guardar_producto", methods=["POST"])
@requiere_rol("administrador")
def guardar_producto():
    imagen, error_imagen = guardar_imagen(request.files.get("imagen"))
    errores, producto = validar_producto(
        request.form.get("codigo"),
        request.form.get("nombre"),
        request.form.get("precio"),
        request.form.get("categoria"),
        imagen,
        True,
    )
    if error_imagen:
        errores.append(error_imagen)
    if errores:
        return render_template("registro_producto.html", errores=errores, **producto)
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT 1 FROM productos WHERE codigo = %s", (producto["codigo"],))
        if cursor.fetchone():
            return render_template("registro_producto.html", errores=["Ya existe un producto con ese código."], **producto)
        cursor.execute(
            "INSERT INTO productos (codigo, nombre, precio, categoria, imagen) VALUES (%s, %s, %s, %s, %s)",
            (producto["codigo"], producto["nombre"], producto["precio"], producto["categoria"], producto["imagen"]),
        )
        conexion.commit()
    except Exception:
        conexion.rollback()
        return render_template("registro_producto.html", errores=["No se pudo guardar el producto."], **producto)
    finally:
        cursor.close()
        conexion.close()
    flash("Producto registrado exitosamente.", "success")
    return redirect(url_for("productos"))


@app.route("/editar_producto/<string:codigo>")
@requiere_rol("administrador")
def editar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
        producto = cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos"))
    return render_template("editar_productos.html", producto=producto)


@app.route("/actualizar_producto", methods=["POST"])
@requiere_rol("administrador")
def actualizar_producto():
    codigo = request.form.get("codigo", "").strip().upper()
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT imagen FROM productos WHERE codigo = %s", (codigo,))
        existente = cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()
    imagen = existente["imagen"] if existente else None
    archivo = request.files.get("imagen")
    if archivo and archivo.filename:
        imagen, error_imagen = guardar_imagen(archivo)
    else:
        error_imagen = None
    errores, producto = validar_producto(
        codigo,
        request.form.get("nombre"),
        request.form.get("precio"),
        request.form.get("categoria"),
        imagen,
    )
    if error_imagen:
        errores.append(error_imagen)
    if errores:
        producto["imagen"] = imagen
        return render_template("editar_productos.html", producto=producto, errores=errores)
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE productos SET nombre = %s, precio = %s, categoria = %s, imagen = %s WHERE codigo = %s",
            (producto["nombre"], producto["precio"], producto["categoria"], imagen, codigo),
        )
        conexion.commit()
        flash("Producto actualizado correctamente.", "success")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("productos"))


@app.route("/eliminar_producto/<string:codigo>", methods=["POST"])
@requiere_rol("administrador")
def eliminar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
        conexion.commit()
        flash("Producto eliminado correctamente.", "success")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("productos"))


@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html", productos=obtener_productos())


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
