from flask import Flask, render_template, request, redirect, url_for, flash
from database.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "clave_super_secreta_techstore"

@app.route("/")
def inicio():
    return render_template("index1.html")

@app.route("/productos")
def productos():
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    cursor.close()

    conexion.close()

    # Formatear precio para mostrarlo con formato de moneda ($ 3,500,000)
    for p in productos:
        try:
            p['precio_formateado'] = f"$ {int(p['precio']):,}"
        except (ValueError, TypeError, KeyError):
            p['precio_formateado'] = f"$ {p.get('precio', 0)}"

    return render_template("productos.html",productos=productos)

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
    return render_template("registro_producto.html")

@app.route("/guardar_producto",methods=["POST"])
def guardar_producto():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]

    exito = False
    mensaje = ""
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
        exito = True
        mensaje = "Producto registrado y guardado con éxito en la base de datos."
    except Exception as e:
        mensaje = f"Error al guardar en la base de datos: {e}"

    return render_template(
        "respuesta.html",
        codigo=codigo,
        nombre=nombre,
        precio=precio,
        categoria=categoria,
        exito=exito,
        mensaje=mensaje
    )

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

    return render_template("editar_productos.html", producto=producto)

@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    codigo = request.form.get("codigo")
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    categoria = request.form["categoria"]

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET nombre = %s, precio = %s, categoria = %s WHERE codigo = %s",
            (nombre, precio, categoria, codigo)
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