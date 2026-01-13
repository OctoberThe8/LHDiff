<?php
session_start();
require_once '../includes/db.php';

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];

    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $user = $stmt->get_result()->fetch_assoc();

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        $_SESSION['is_admin'] = $user['is_admin'];

        // Load cart from DB
        $uid = $user['id'];
        $_SESSION['cart'][$uid] = [];
        $stmt = $conn->prepare("SELECT book_id, quantity FROM carts WHERE user_id = ?");
        $stmt->bind_param("i", $uid);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $_SESSION['cart'][$uid][$row['book_id']] = $row['quantity'];
        }
        header("Location: profile.php");
        exit();
    } else {
        $error = 'Invalid credentials';
    }
}
?>

<?php include '../includes/header.php'; ?>
<h2>Login</h2>
<p style="color:red;"><?= $error ?></p>
<form method="POST">
    Username: <input type="text" name="username" required><br>
    Password: <input type="password" name="password" required><br>
    <button type="submit">Login</button>
</form>
<?php include '../includes/footer.php'; ?>