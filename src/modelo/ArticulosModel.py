from modelo.coneccion import db_connection
from flask import jsonify, request

class ArticuloModel:
    @classmethod
    def listar_articulos(cls):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select id, nombre, descripcion, cantidad, precio from articulos""")
            datos = cur.fetchall()
            articulos = []
            for fila in datos:
                articulo = {
                    'id': fila[0],
                    'nombre': fila[1],
                    'descripcion': fila[2],
                    'cantidad': fila[3],
                    'precio': fila[4]
                }
                articulos.append(articulo)
            conn.close()
            return jsonify({'Articulos': articulos, 'mensaje': "Articulos listados.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def buscar_articulo(cls, codigo):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select id, nombre, descripcion, cantidad, precio from articulos where id = %s""",
                        (codigo,))
            datos = cur.fetchone()
            conn.close()
            if datos is not None:
                articulo = {
                    'id': datos[0],
                    'nombre': datos[1],
                    'descripcion': datos[2],
                    'cantidad': datos[3],
                    'precio': datos[4]
                }
                return articulo
            else:
                return None
        except Exception as ex:
            raise ex

    @classmethod
    def crear_articulo(cls):
        try:
            articulo = cls.buscar_articulo(request.json['id'])
            if articulo is not None:
                return jsonify({'mensaje': "Id de articulo ya existe"})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute('insert into articulos values (%s, %s, %s, %s, %s)',
                            (request.json['id'],
                             request.json['nombre'],
                             request.json['descripcion'],
                             request.json['cantidad'],
                             request.json['precio'])
                            )
                conn.commit()
                conn.close()
                return jsonify({'mensaje': 'Articulo registrado', 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': 'Error', 'exito': False})
    
    @classmethod
    def borrar_articulo(cls,codigo):
        try:
            articulo = cls.buscar_articulo(codigo)
            if articulo is not None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("delete from articulos where id = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': 'Articulo eliminado', 'exito': True})
            else:
                return jsonify({'mensaje': 'No existe el id', 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': 'Error', 'exito': False})
    @classmethod
    def actualizar_articulo(cls, codigo):
        try:
            product = cls.buscar_articulo(codigo)
            if product is not None:
                con = db_connection()
                cur = con.cursor()
                cur.execute("update articulos set nombre=%s, descripcion=%s, cantidad= %s, precio=%s where id=%s",
                    (
                        request.json["nombre"],
                        request.json["descripcion"],
                        request.json["cantidad"],
                        request.json["precio"],
                        codigo,
                    ),
                )
                con.commit()
                con.close()
                return jsonify(
                    {
                        "message": "articulo actualizado",
                        "exito": True,
                    }
                )
            else:
                return jsonify({"message": "articulo no encontrado", "exito": True})
        except Exception as e:
            raise jsonify({"message": "error", "exito": False})

   
