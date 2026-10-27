import os

import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def obtener_conexion():
    """Conecta a PostgreSQL usando la URL privada de Render."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Falta configurar la variable de entorno DATABASE_URL")
    return psycopg2.connect(database_url)


@app.get("/")
def estado():
    return jsonify({"estado": "ok", "servicio": "Centinela Digital API"})


@app.post("/api/reportes")
def crear_reporte():
    datos = request.get_json(silent=True) or {}
    tipo_registro = datos.get("tipo_registro")
    rol_usuario = datos.get("rol_usuario")

    if not tipo_registro or not rol_usuario:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reportes (tipo_registro, rol_usuario)
                VALUES (%s, %s)
                RETURNING id, tipo_registro, rol_usuario, fecha
                """,
                (tipo_registro, rol_usuario),
            )
            reporte = cursor.fetchone()
        conexion.commit()
        return jsonify(
            {
                "mensaje": "Reporte registrado correctamente",
                "reporte": {
                    "id": reporte[0],
                    "tipo_registro": reporte[1],
                    "rol_usuario": reporte[2],
                    "fecha": reporte[3].isoformat(),
                },
            }
        ), 201
    except Exception as error:
        if conexion:
            conexion.rollback()
        app.logger.exception("No se pudo crear el reporte")
        return jsonify({"error": "No se pudo registrar el reporte"}), 500
    finally:
        if conexion:
            conexion.close()


@app.delete("/api/reportes/<int:reporte_id>")
def eliminar_reporte(reporte_id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM reportes WHERE id = %s", (reporte_id,))
            eliminado = cursor.rowcount
        conexion.commit()
        if not eliminado:
            return jsonify({"error": "Reporte no encontrado"}), 404
        return jsonify({"mensaje": "Reporte eliminado correctamente"})
    except Exception as error:
        if conexion:
            conexion.rollback()
        app.logger.exception("No se pudo eliminar el reporte")
        return jsonify({"error": "No se pudo eliminar el reporte"}), 500
    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
