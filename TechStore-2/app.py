import re
from decimal import Decimal, InvalidOperation

from flask import Flask, render_template, request, redirect, url_for, flash
from database.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "clave_super_secreta_techstore"


def formatear_precio(precio):
    try:
        return f"$ {int(precio):,}"
    except (ValueError, TypeError, KeyError):
        return f"$ {precio}"


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


def validar_datos_producto(datos):
    errores = []
    codigo = (datos.get("codigo") or "").strip()
    nombre = (datos.get("nombre") or "").strip()
    precio = (datos.get("precio") or "").strip()
    categoria = (datos.get("categoria") or "").strip()

    if not codigo:
        errores.append("El código del producto es obligatorio.")
    elif not re.fullmatch(r"\d+", codigo):
        errores.append("El código del producto solo debe contener números.")

    if not nombre:
        errores.append("El nombre del producto es obligatorio.")
    elif re.search(r"\d", nombre):
        errores.append("El nombre no debe contener números.")

    if not categoria:
        errores.append("La categoría es obligatoria.")
    elif re.search(r"\d", categoria):
        errores.append("La categoría no debe contener números.")

    if not precio:
        errores.append("El precio es obligatorio.")
    else:
        if re.fullmatch(r"-\d+(?:\.\d{1,2})?", precio):
            errores.append("El precio no puede ser negativo.")
        elif not re.fullmatch(r"\d+(?:\.\d{1,2})?", precio):
            errores.append("El precio debe ser un número válido.")
        else:
            try:
                precio_valor = Decimal(precio)
                if precio_valor < 0:
                    errores.append("El precio no puede ser negativo.")
            except InvalidOperation:
                errores.append("El precio debe ser un número válido.")

    return errores


@app.route("/")
def inicio():
    productos = obtener_productos()
    return render_template("index1.html", productos=productos)

@app.route("/productos")
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
def registro_producto():
    return render_template("registro_producto.html", editar=False, errores=[])

@app.route("/guardar_producto",methods=["POST"])
def guardar_producto():
    codigo = request.form.get("codigo", "").strip()
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
def actualizar_producto():
    codigo_original = request.form.get("codigo_original", "").strip()
    codigo = request.form.get("codigo", "").strip()
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