from flask import Flask

app = Flask(__name__)

@app.route("/inventario")
def inventario():
    return 'sistema inventario activo'

if __name__ == '__main__':
    app.run(debug=True)
