<?php
// Configuramos los encabezados para que responda estrictamente en formato JSON
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Access-Control-Allow-Methods: POST");

$servidor = "localhost";
$usuario  = "root";
$password = ""; 
$base_datos = "centinela_bd"; 

$conexion = new mysqli($servidor, $usuario, $password, $base_datos);

if ($conexion->connect_error) {
    echo json_encode(["error" => "Error de conexión: " . $conexion->connect_error]);
    exit();
}

// Leemos el JSON enviado desde el Frontend (como lo hace req.body en tu apunte)
$datosRecibidos = json_decode(file_get_contents("php://input"), true);

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($datosRecibidos['tipo_registro'])) {
    $tipo_registro = $datosRecibidos['tipo_registro'];
    $rol_usuario   = $datosRecibidos['rol_usuario'];

    // 1. Guardar en la base de datos
    $sql = "INSERT INTO reportes (tipo_registro, rol_usuario) VALUES (?, ?)";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param("ss", $tipo_registro, $rol_usuario);

    if ($stmt->execute()) {
        // 2. Enviar Respuesta con Código de Estado 201 Created y estructura JSON
        http_response_code(201);
        echo json_encode([
            "mensaje" => "Pedido registrado correctamente", // Mismo mensaje de tu apunte
            "reporte" => [
                "id" => $conexion->insert_id,
                "tipo_registro" => $tipo_registro,
                "rol_usuario" => $rol_usuario,
                "fecha" => date("Y-m-d H:i:s")
            ]
        ]);
    } else {
        http_response_code(500);
        echo json_encode(["error" => "No se pudo registrar el reporte"]);
    }
    $stmt->close();
} else {
    http_response_code(400);
    echo json_encode(["error" => "Datos inválidos o método no permitido"]);
}
$conexion->close();
?>
