import re
from decimal import Decimal, InvalidOperation

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from database.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "clave_super_secreta_techstore"


def login_required(f):
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para acceder a esta página.", "error")
            return redirect(url_for("inicio"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def admin_required(f):
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para acceder a esta página.", "error")
            return redirect(url_for("inicio"))
        if session.get("rol") != "Administrador":
            flash("No tienes permisos de administrador.", "error")
            return redirect(url_for("inicio"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def formatear_precio(precio):
    try:
        return f"$ {int(precio):,}"
    except (ValueError, TypeError, KeyError):
        return f"$ {precio}"


def verificar_password(password_almacenado, password_ingresado):
    if not password_almacenado:
        return False
    if isinstance(password_almacenado, str) and (
        password_almacenado.startswith("scrypt:") or password_almacenado.startswith("pbkdf2:")
    ):
        return check_password_hash(password_almacenado, password_ingresado)
    return password_almacenado == password_ingresado


def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY nombre")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()

    for producto in productos:
        producto["precio_formateado"] = formatear_precio(producto.get("precio", 0))

    return productos


def validar_datos_producto(datos, codigo_original=None):
    errores = []
    codigo = (datos.get("codigo") or "").strip().upper()
    nombre = (datos.get("nombre") or "").strip()
    precio = (datos.get("precio") or "").strip()
    categoria = (datos.get("categoria") or "").strip()

    if not codigo:
        errores.append("El código del producto es obligatorio.")
    else:
        if len(codigo) < 5 and not re.fullmatch(r"P\d{3}", codigo):
            errores.append("El código debe tener al menos 5 caracteres.")
        if not re.fullmatch(r"P\d{3,}", codigo):
            errores.append("El código debe tener el formato P001.")

    if not nombre:
        errores.append("El nombre del producto es obligatorio.")
    else:
        if len(nombre) < 5:
            errores.append("El nombre debe tener al menos 5 caracteres.")
        if len(nombre) > 100:
            errores.append("El nombre no puede exceder los 100 caracteres.")

    if not categoria:
        errores.append("La categoría es obligatoria.")

    if not precio:
        errores.append("El precio del producto es obligatorio.")
    else:
        if not re.fullmatch(r"\d+(?:\.\d{1,2})?", precio):
            errores.append("El precio debe ser un número válido.")
        else:
            try:
                precio_valor = Decimal(precio)
                if precio_valor <= 0:
                    errores.append("El precio debe ser mayor que cero.")
                elif precio_valor > Decimal("5000000"):
                    errores.append("El precio no puede ser mayor a 5000000.")
            except InvalidOperation:
                errores.append("El precio debe ser un número válido.")

    if codigo:
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT codigo FROM productos WHERE codigo = %s", (codigo,))
            producto_existente = cursor.fetchone()
            cursor.close()
            conexion.close()
            if producto_existente and (codigo_original is None or producto_existente["codigo"] != codigo_original):
                errores.append("El código del producto ya existe.")
        except Exception:
            pass

    return errores


@app.route("/")
def inicio():
    productos = obtener_productos()
    return render_template("index1.html", productos=productos)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip()
        contraseña = request.form.get("contraseña", "")

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        password_almacenado = (usuario.get("contrasena") if usuario else None) or (usuario.get("contraseña") if usuario else None) or ""

        if usuario and verificar_password(password_almacenado, contraseña):
            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]
            flash("Inicio de sesión exitoso.", "success")
            if usuario["rol"] == "Administrador":
                return redirect("/admin.html")
            return redirect("/")

        flash("Correo o contraseña incorrectos.", "error")

    return render_template("login.html")

@app.route("/registro_usuario", methods=["GET", "POST"])
def registro_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        contraseña = request.form.get("contraseña", "")
        confirmar = request.form.get("confirmar_contraseña", "")

        if not nombre or not correo or not contraseña:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("registro_usuario.html")

        if contraseña != confirmar:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("registro_usuario.html")

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
        if cursor.fetchone():
            cursor.close()
            conexion.close()
            flash("El correo ya está registrado.", "error")
            return render_template("registro_usuario.html")

        password_hash = generate_password_hash(contraseña)
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena, rol, estado) VALUES (%s, %s, %s, %s, %s)",
            (nombre, correo, password_hash, "usuario", "Activo"),
        )
        conexion.commit()
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()

        session["usuario_id"] = usuario["id"]
        session["nombre"] = usuario["nombre"]
        session["rol"] = usuario["rol"]
        flash("Registro exitoso. Ya puedes usar la tienda.", "success")
        return redirect("/")

    return render_template("registro_usuario.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("inicio"))

@app.route("/admin")
@app.route("/admin.html")
@admin_required
def admin():
    return render_template("admin.html")

@app.route("/productos")
@app.route("/productos.html")
@admin_required
def productos():
    productos = obtener_productos()
    return render_template("productos.html", productos=productos)

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html")

@app.route("/registro_producto")
@admin_required
def registro_producto():
    return render_template("registro_producto.html", editar=False, errores=[])

@app.route("/guardar_producto",methods=["POST"])
@admin_required
def guardar_producto():
    codigo = request.form.get("codigo", "").strip().upper()
    nombre = request.form.get("nombre", "").strip()
    precio = request.form.get("precio", "").strip()
    categoria = request.form.get("categoria", "").strip()

    errores = validar_datos_producto({
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria,
    })

    if errores:
        for error in errores:
            flash(error, "error")
        return render_template(
            "registro_producto.html",
            editar=False,
            errores=errores,
            datos={
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria,
            },
        )

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (codigo, nombre, precio, categoria) VALUES (%s, %s, %s, %s)",
            (codigo, nombre, precio, categoria)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("productos"))
    except Exception as e:
        flash(f"Error al guardar en la base de datos: {e}", "error")
        return redirect(url_for("registro_producto"))

@app.route("/editar_producto/<string:codigo>")
@admin_required
def editar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos"))

    return render_template("editar_productos.html", producto=producto, errores=[])

@app.route("/actualizar_producto", methods=["POST"])
@admin_required
def actualizar_producto():
    codigo_original = request.form.get("codigo_original", "").strip().upper()
    codigo = request.form.get("codigo", "").strip().upper()
    nombre = request.form.get("nombre", "").strip()
    precio = request.form.get("precio", "").strip()
    categoria = request.form.get("categoria", "").strip()

    errores = validar_datos_producto({
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria,
    }, codigo_original=codigo_original)

    if errores:
        for error in errores:
            flash(error, "error")
        return render_template(
            "editar_productos.html",
            producto={
                "codigo": codigo_original,
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria,
            },
            errores=errores,
        )

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = %s, precio = %s, categoria = %s WHERE codigo = %s",
            (nombre, precio, categoria, codigo_original)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Producto actualizado correctamente.", "success")
    except Exception as e:
        flash(f"No se pudo actualizar el producto: {e}", "error")

    return redirect(url_for("productos"))

@app.route("/eliminar_producto/<string:codigo>")
@admin_required
def eliminar_producto(codigo):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Producto eliminado correctamente.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar el producto: {e}", "error")

    return redirect(url_for("productos"))

if __name__ == "__main__":
    app.run(debug=True)

# TechStore/
# │
# ├── app.py
# │
# ├── templates/
# │   ├── index.html
# │   ├── registro_producto.html
# │   └── respuesta.html
# │
# └── static/