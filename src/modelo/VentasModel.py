from modelo.coneccion import db_connection
from flask import jsonify, request
from modelo.ArticulosModel import ArticuloModel

class VentaModel():
    @classmethod
    def listar_venta(CLS):
        try:
            con=db_connection()
            cur=con.cursor()
            cur.execute("""select * from ventas""")
            datos=cur.fetchall()
            ventas=[]
            for fila in datos:
                venta={
                    "id_fac": fila[0],
                    "pago":fila[1],
                    "id":fila[2]
                }
                ventas.append(venta)
            con.close()
            return jsonify({"Ventas":ventas,"mensaje":"Ventas listadas","exito":True})
        except Exception as ex:
            return jsonify({"Mensaje":"Error","Exito":False})
    
    @classmethod
    def buscar_venta(cls, id):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select * from ventas where id_fac = %s""",(id,))
            datos = cur.fetchone()
            conn.close()
            if datos is not None:
                venta = {
                    'id_fac': datos[0],
                    'pago': datos[1],
                    'id':datos[2]
                }
                return venta
            else:
                return None
        except Exception as ex:
            raise ex

    @classmethod
    def crear_venta(cls):
        try:
            venta = cls.buscar_venta(request.json['id_fac'])
            if venta is not None:
                return jsonify({'mensaje': "Id de factura ya existe"})
            else:
                articulo =ArticuloModel.buscar_articulo(request.json['id'])
                if articulo is not None:
                    conn = db_connection()
                    cur = conn.cursor()
                    cur.execute('insert into ventas values (%s, %s, %s)',
                                (request.json['id_fac'],
                                 request.json['pago'],
                                 request.json['id'],
                                ))
                    conn.commit()
                    conn.close()
                    return jsonify({'mensaje': 'Venta registrada', 'exito': True})
                else:
                    return jsonify({"mensaje":"el id de la factura no existe","exito":False})
        except Exception as ex:
            return jsonify({'mensaje': 'Error', 'exito': False})
    
    @classmethod
    def borrar_venta(cls,codigo):
        try:
            venta = cls.buscar_venta(codigo)
            if venta is not None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("delete from ventas where id_fac = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': 'Articulo eliminado', 'exito': True})
            else:
                return jsonify({'mensaje': 'No existe el id', 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': 'Error', 'exito': False})
    @classmethod
    def actualizar_venta(cls, codigo):
        try:
            product = cls.buscar_venta(codigo)
            if product is not None:
                con = db_connection()
                cur = con.cursor()
                cur.execute("update ventas set pago=%s, id=%s where id_fac=%s",
                    (
                        request.json["pago"],
                        request.json["id"],
                        codigo,
                    )
                )
                con.commit()
                con.close()
                return jsonify(
                    {
                        "message": "venta actualizado",
                        "exito": True,
                    }
                )
            else:
                return jsonify({"message": "venta no encontrado", "exito": True})
        except Exception as ex:
            return jsonify({"message": "error", "exito": False})
    @classmethod
    def contador(cls):
        try:
            con=db_connection()
            cur=con.cursor()
            cur.execute('select ventas.id as articulo,count(ventas.id) as cant_ventas from ventas,articulos where ventas.id=articulos.id group by ventas.id');
            datos=cur.fetchall()
            ventas=[]
            for fila in datos:
                venta={
                    "articulo":fila[0],
                    "cant_ventas":fila[1]
                }
                ventas.append(venta)
            con.close()
            return jsonify({"Ventas":ventas,"mensaje":"cantidad de ventas por articulo listadas","exito":True})
        except Exception as ex:
            return jsonify({"message": "error", "exito": False})