from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
# Esto da permiso absoluto para que tu formulario HTML se conecte sin bloqueos
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Conexión local a tu MySQL de XAMPP
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Déjalo vacío si usas XAMPP por defecto
        database="centinela_bd"
    )

@app.route('/api/reportes', methods=['POST'])
def crear_reporte():
    try:
        datos = request.json
        tipo_registro = datos.get('tipo_registro')
        rol_usuario = datos.get('rol_usuario')
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = "INSERT INTO reportes (tipo_registro, rol_usuario) VALUES (%s, %s)"
        cursor.execute(query, (tipo_registro, rol_usuario))
        conexion.commit()
        
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        
        return jsonify({
            "mensaje": "Pedido registrado correctamente",
            "reporte": {
                "id": nuevo_id,
                "tipo_registro": tipo_registro,
                "rol_usuario": rol_usuario,
                "fecha": "Hoy"
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2ª Solicitud HTTP: Eliminar Registro (DELETE)
@app.route('/api/reportes/<int:id>', methods=['DELETE'])
def eliminar_reporte(id):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = "DELETE FROM reportes WHERE id = %s"
        cursor.execute(query, (id,))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "Registro eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
