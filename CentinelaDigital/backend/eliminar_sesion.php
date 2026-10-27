<?php
header("Access-Control-Allow-Origin: *");
$servidor = "localhost";
$usuario  = "root";
$password = ""; 
$base_datos = "centinela_bd"; 

$conexion = new mysqli($servidor, $usuario, $password, $base_datos);

if (isset($_GET['id'])) {
    $reporte_id = intval($_GET['id']);
    
    $sql = "DELETE FROM reportes WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param("i", $reporte_id);
    $stmt->execute();
    $stmt->close();
    echo "Eliminado";
}
$conexion->close();
?>
