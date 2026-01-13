<?php
// Displays and processes the login form
// Authenticates users with hashed passwords and initializes session state
// Loads the user's saved cart into session and redirects on success

session_start();
require_once '../includes/db.php';

// Set SEO metadata for the Login page
$pageTitle = "WonderGoof: Login";
$pageDescription = "Access your WonderGoof account to view your cart, order history, and profile.";
$pageKeywords = "login, WonderGoof account, children bookstore login";

$error = '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];

    // Fetch user by username
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $user = $stmt->get_result()->fetch_assoc();

    // Verify password and initialize session
    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        $_SESSION['is_admin'] = $user['is_admin'];

        // Initialize empty cart session array for this user
        $uid = $user['id'];
        $_SESSION['cart'][$uid] = [];

        // Load saved cart items from database
        $stmt = $conn->prepare("SELECT format_id, quantity FROM carts WHERE user_id = ?");
        $stmt->bind_param("i", $uid);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            $_SESSION['cart'][$uid][$row['format_id']] = $row['quantity'];
        }
        // Redirect with sound effect on success
        echo '<script>
            localStorage.setItem("playLoginSound", "true");
            window.location.href = "profile.php";
        </script>';
        exit;
    } else {
        // Show error if authentication fails
        $error = 'Invalid credentials';
    }
}
?>

<?php include '../includes/header.php'; ?>

<!-- Login Form UI -->
<h2 class="general-centered-heading">Login</h2>
<div class="form-wrapper">
    <form class="contact-form" method="post" action="login.php">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required>

        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required>

        <!-- Show error message if login failed -->
        <?php if (!empty($error)): ?>
            <div class="message"><?= htmlspecialchars($error) ?></div>
        <?php endif; ?>

        <br><br>
        <button type="submit">Login</button>
    </form>
</div>

<?php include '../includes/footer.php'; ?>