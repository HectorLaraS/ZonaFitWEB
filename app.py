from flask import Flask, render_template, jsonify, redirect, url_for
from cliente_dao import ClienteDAO
from cliente import Cliente
from cliente_forma import ClienteForma
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

titulo_app = "ZonaFit (GYM)"

@app.route("/")
def home():
    app.logger.debug("entramos al path de home ")
    clientes_db: list[Cliente] = ClienteDAO.seleccionar()
    cliente = Cliente()
    cliente_forma = ClienteForma(obj=cliente)
    return render_template("index.html", titulo=titulo_app, clientes=clientes_db, forma=cliente_forma)

@app.route("/guardar", methods=["POST"])
def guardar():
    cliente = Cliente()
    cliente_forma = ClienteForma(obj=cliente)
    if cliente_forma.validate_on_submit():
        cliente_forma.populate_obj(cliente)
        if not cliente.id:
            ClienteDAO.insertar(cliente)
        else:
            ClienteDAO.actualizar(cliente)
    return redirect(url_for("home"))


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


@app.route("/limpiar")
def limpiar():
    return redirect(url_for("home"))

@app.route("/editar/<int:id>")
def editar(id: int):
    cliente: Cliente = ClienteDAO.seleccionar_id(id)
    cliente_forma = ClienteForma(obj=cliente)
    clientes_db: list[Cliente] = ClienteDAO.seleccionar()
    return render_template('index.html',titulo=titulo_app, clientes=clientes_db, forma=cliente_forma)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
