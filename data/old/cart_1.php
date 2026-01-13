<?php
session_start();
require_once '../includes/db.php';
require_once '../includes/header.php';

// Initialize cart
if (!isset($_SESSION['cart'])) {
    $_SESSION['cart'] = [];
}

// Handle add-to-cart
if (isset($_GET['add'])) {
    $book_id = (int)$_GET['add'];
    if (!isset($_SESSION['cart'][$book_id])) {
        $_SESSION['cart'][$book_id] = 1;
    } else {
        $_SESSION['cart'][$book_id]++;
    }
    $ref = $_SERVER['HTTP_REFERER'] ?? 'cart.php';
    header("Location: $ref");
    exit;
}

// Handle quantity updates
if (isset($_GET['update']) && isset($_GET['id']) && isset($_GET['qty'])) {
    $book_id = (int)$_GET['id'];
    $qty = max(0, (int)$_GET['qty']);   // Ensure no negative quantity
    if ($qty == 0) {
        unset($_SESSION['cart'][$book_id]);
    } else {
        $_SESSION['cart'][$book_id] = $qty;
    }
    header("Location: cart.php");
    exit;
}

// Handle remove-from-cart
if (isset($_GET['remove'])) {
    $book_id = (int)$_GET['remove'];
    unset($_SESSION['cart'][$book_id]);
    header("Location: cart.php");
    exit;
}

// Fetch book data
$books_in_cart = [];
$total = 0;

if (!empty($_SESSION['cart'])) {
    $ids = implode(',', array_keys($_SESSION['cart']));
    $stmt = $conn->query("SELECT * FROM books WHERE id IN ($ids)");
    while ($book = $stmt->fetch_assoc()) {
        $book['quantity'] = $_SESSION['cart'][$book['id']];
        $book['subtotal'] = $book['price'] * $book['quantity'];
        $total += $book['subtotal'];
        $books_in_cart[] = $book;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Your Cart</title>
    <link rel="stylesheet" href="../css/main.css">
</head>
<body>
<h2>Your Shopping Cart</h2>

<?php if (empty($books_in_cart)): ?>
    <p>Your cart is empty.</p>
<?php else: ?>
    <table border="1">
        <tr>
            <th>Image</th>
            <th>Title</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Subtotal</th>
            <th>Remove</th>
        </tr>
        <?php foreach ($books_in_cart as $book): ?>
            <tr>
                <td><img src="../assets/books/<?= htmlspecialchars($book['cover_image']) ?>" width="60"></td>
                <td><?= htmlspecialchars($book['title']) ?></td>
                <td>
                    <button onclick="updateQty(<?= $book['id'] ?>, <?= $book['quantity'] - 1 ?>)" <?= $book['quantity'] == 1 ? 'disabled' : '' ?>>-</button>
                    <span id="qty-<?= $book['id'] ?>"><?= $book['quantity'] ?></span>
                    <button onclick="updateQty(<?= $book['id'] ?>, <?= $book['quantity'] + 1 ?>)">+</button>
                </td>
                <td>$<span id="price-<?= $book['id'] ?>"><?= number_format($book['price'], 2) ?></span></td>
                <td>$<span id="subtotal-<?= $book['id'] ?>"><?= number_format($book['subtotal'], 2) ?></span></td>
                <td><a href="cart.php?remove=<?= $book['id'] ?>">Remove</a></td>
            </tr>
        <?php endforeach; ?>
        <tr>
            <td colspan="4"><strong>Total:</strong></td>
            <td>$<?= number_format($total, 2) ?></td>
            <td colspan="2"></td>
        </tr>
    </table>
    <br>
    <a href="checkout.php">Proceed to Checkout</a>
<?php endif; ?>
<script>
function updateQty(id, newQty) {
    if (newQty < 1 || newQty > 99) return;

    fetch('cart.php?update=1&id=' + id + '&qty=' + newQty)
        .then(response => response.text())
        .then(() => location.reload()); // Reload to reflect new data
}
</script>
</body>
</html>

<?php require_once '../includes/footer.php'; ?>