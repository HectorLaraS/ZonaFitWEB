from flask import Flask, render_template, jsonify
from cliente_dao import ClienteDAO
from cliente import Cliente

app = Flask(__name__)

titulo_app = "ZonaFit (GYM)"

@app.route("/")
def home():
    app.logger.debug("entramos al path de home ")
    clientes_db: list[Cliente] = ClienteDAO.seleccionar()
    return render_template("index.html", titulo=titulo_app, clientes=clientes_db)

@app.route("/api/clientes", methods=["GET"])
def obtener_clientes():
    clientes_db: list[Cliente] = ClienteDAO.seleccionar()
    clientes_dict:list = [ cliente.to_dict() for cliente in clientes_db]
    return jsonify(clientes_dict)

@app.route("/api/clientes/<int:id>", methods=["GET"])
def obtener_cliente(id):
    clientes_db: list[Cliente] = ClienteDAO.seleccionar()
    for cliente in clientes_db:
        if cliente.id == id:
            return jsonify(cliente.to_dict())
    return jsonify({"error":"cliente no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
