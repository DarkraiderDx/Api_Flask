from flask import Flask, jsonify, request
from flask_cors import CORS
from modelo.ArticulosModel import ArticuloModel
from modelo.VentasModel import VentaModel

app = Flask(__name__)

CORS(app,resources={r"/articulos/*":{"origins": "https://proyecto-modulo3.onrender.com"}})
CORS(app,resources={r"/ventas/*":{"origins": "https://proyecto-modulo3.onrender.com"}})

@app.route('/')
def hola():
    return "404 Not Found"

@app.route('/articulos', methods=['GET'])
def listar_articulo():
    art = ArticuloModel.listar_articulos()
    return art

@app.route('/articulos', methods=['POST'])
def crear_articulos():
    art = ArticuloModel.crear_articulo()
    return art
@app.route('/articulos:<codigo>', methods=['DELETE'])
def borrar_articulos(codigo):
    art=ArticuloModel.borrar_articulo(codigo)
    return art
@app.route('/articulos:<codigo>',methods=['PUT'])
def actualizar_articulos(codigo):
    art=ArticuloModel.actualizar_articulo(codigo)
    return art
@app.route('/ventas',methods=['GET'])
def listar_ventas():
    vent=VentaModel.listar_venta()
    return vent
@app.route('/ventas',methods=['POST'])
def crear_ventas():
    vent=VentaModel.crear_venta()
    return vent
@app.route('/ventas:<codigo>',methods=['DELETE'])
def borrar_ventas(codigo):
    vent=VentaModel.borrar_venta(codigo)
    return vent
@app.route('/ventas:<codigo>',methods=['PUT'])
def actualizar_ventas(codigo):
    vent=VentaModel.actualizar_venta(codigo)
    return vent
@app.route('/reporte',methods=['GET'])
def reporte():
    rep=VentaModel.contador()
    return rep
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
