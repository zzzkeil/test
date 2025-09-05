<?php
$pdo = new PDO("mysql:host=localhost;dbname=n;charset=utf8", "u", "p");

// Fetch POIs
if ($_GET['action'] === 'get_pois') {
    $stmt = $pdo->query("SELECT id, name, longitude, latitude FROM pois");
    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
    exit;
}

// Save Booking
if ($_POST['action'] === 'book') {
    $stmt = $pdo->prepare("INSERT INTO bookings (poi_id, customer_name, customer_email) VALUES (?, ?, ?)");
    $stmt->execute([$_POST['poi_id'], $_POST['name'], $_POST['email']]);
    echo json_encode(["status" => "success"]);
    exit;
}
