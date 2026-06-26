from flask import Flask, render_template, request
from database.conexion import obtener_conexion

app = Flask(__name__)

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