from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'Bienvenido al sistema'

@app.route('/saludo')
def saludo():
    return 'Hola aprendiz ADSO!'

@app.route('/productos')
def productos():
    return 'Lista de productos'

@app.route('/inventario')
def inventario():
    return 'sistema inventario activo'

if __name__ == '__main__':
    app.run(debug=True)
