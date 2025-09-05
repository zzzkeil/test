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

// Fetch Bookings (with POI name)
if ($_GET['action'] === 'get_bookings') {
    $stmt = $pdo->query("
        SELECT b.id, p.name AS poi_name, b.customer_name, b.customer_email, b.booking_time
        FROM bookings b
        JOIN pois p ON b.poi_id = p.id
        ORDER BY b.booking_time DESC
    ");
    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
    exit;
}

// Delete Booking
if ($_POST['action'] === 'delete_booking') {
    $stmt = $pdo->prepare("DELETE FROM bookings WHERE id = ?");
    $stmt->execute([$_POST['id']]);
    echo json_encode(["status" => "deleted"]);
    exit;
}
