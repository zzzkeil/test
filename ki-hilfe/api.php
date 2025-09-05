<?php
header("Content-Type: application/json; charset=utf-8");

$dsn = "mysql:host=localhost;dbname=poiapp;charset=utf8mb4";
$user = "poiuser";   // anpassen
$pass = "geheim";    // anpassen

try {
    $pdo = new PDO($dsn, $user, $pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => $e->getMessage()]);
    exit;
}

$method = $_SERVER["REQUEST_METHOD"];

if ($method === "GET" && isset($_GET["poi"])) {
    // Alle Einträge zu einem POI
    $stmt = $pdo->prepare("SELECT * FROM entries WHERE poi = ? ORDER BY date,time");
    $stmt->execute([$_GET["poi"]]);
    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));

} elseif ($method === "POST" && isset($_GET["poi"])) {
    // Neuen Eintrag speichern
    $data = json_decode(file_get_contents("php://input"), true);
    if (!$data) { http_response_code(400); exit; }
    $stmt = $pdo->prepare("INSERT INTO entries (poi,name,date,time) VALUES (?,?,?,?)");
    $stmt->execute([$_GET["poi"], $data["name"], $data["date"], $data["time"]]);
    echo json_encode(["success" => true, "id" => $pdo->lastInsertId()]);

} elseif ($method === "PUT" && isset($_GET["id"])) {
    // Eintrag aktualisieren
    $data = json_decode(file_get_contents("php://input"), true);
    if (!$data) { http_response_code(400); exit; }
    $stmt = $pdo->prepare("UPDATE entries SET name=?, date=?, time=? WHERE id=?");
    $stmt->execute([$data["name"], $data["date"], $data["time"], $_GET["id"]]);
    echo json_encode(["success" => true]);

} elseif ($method === "DELETE" && isset($_GET["id"])) {
    // Eintrag löschen
    $stmt = $pdo->prepare("DELETE FROM entries WHERE id=?");
    $stmt->execute([$_GET["id"]]);
    echo json_encode(["success" => true]);

} else {
    http_response_code(400);
    echo json_encode(["error" => "Ungültige Anfrage"]);
}
