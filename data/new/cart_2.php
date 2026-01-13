<?php
// Displays the current user's shopping cart with book info and totals
// Supports adding, updating, and removing items using session-based storage
// Dynamically adjusts quantities via JavaScript and keeps totals updated live

session_start();
require_once '../includes/db.php';
require_once '../includes/auth.php';
require_login();

// Set SEO metadata for the Cart page
$pageTitle = "WonderGoof: Your Cart";
$pageDescription = "View the books you have added to your cart. Adjust quantities or proceed to checkout at WonderGoof.";
$pageKeywords = "shopping cart, WonderGoof books, checkout, buy children books";

require_once '../includes/header.php';

// Initialize cart
$uid = $_SESSION['user_id'];
if (!isset($_SESSION['cart'][$uid])) {
    $_SESSION['cart'][$uid] = [];
}

// Handle add-to-cart
if (isset($_GET['add'])) {
    $format_id = (int)$_GET['add'];
    if ($format_id > 0) {
        if (!isset($_SESSION['cart'][$uid][$format_id])) {
            $_SESSION['cart'][$uid][$format_id] = 1;
        } else {
            $_SESSION['cart'][$uid][$format_id]++;
        }
    }
    $ref = $_SERVER['HTTP_REFERER'] ?? 'cart.php';
    header("Location: $ref");
    exit;
}

// Handle quantity updates
if (isset($_GET['update']) && isset($_GET['id']) && isset($_GET['qty'])) {
    $format_id = (int)$_GET['id'];
    $qty = max(0, (int)$_GET['qty']);
    if ($qty == 0) {
        unset($_SESSION['cart'][$uid][$format_id]);
    } else {
        $_SESSION['cart'][$uid][$format_id] = $qty;
    }
    header("Location: cart.php");
    exit;
}
// Handle remove-from-cart
if (isset($_GET['remove'])) {
    $format_id = (int)$_GET['remove'];
    unset($_SESSION['cart'][$uid][$format_id]);
    header("Location: cart.php");
    exit;
}
// Fetch book data
$books_in_cart = [];
$total = 0;

if (!empty($_SESSION['cart'][$uid])) {
    $ids = implode(',', array_keys($_SESSION['cart'][$uid]));
    $stmt = $conn->query("
        SELECT bf.id, bf.format, bf.price, bf.book_id,
            b.title, b.cover_image
        FROM book_formats bf
        JOIN books b ON bf.book_id = b.id
        WHERE bf.id IN ($ids)
    ");
    while ($row = $stmt->fetch_assoc()) {
        $row['quantity'] = $_SESSION['cart'][$uid][$row['id']];
        $row['subtotal'] = $row['price'] * $row['quantity'];
        $total += $row['subtotal'];
        $books_in_cart[] = $row;
    }
}
?>

<h2>Your Shopping Cart</h2>

<?php if (empty($books_in_cart)): ?>
    <p>Your cart is empty.</p>
<?php else: ?>
    <table class="cart-table">
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
                <td><?= htmlspecialchars($book['title']) ?> (<?= htmlspecialchars($book['format']) ?>)</td>
                <td>
                    <button onclick="changeQty(<?= $book['id'] ?>, -1)" <?= $book['quantity'] == 1 ? 'disabled' : '' ?>>-</button>
                    <input type="number" id="qty-<?= $book['id'] ?>" value="<?= $book['quantity'] ?>" min="1" max="99" oninput="setQty(<?= $book['id'] ?>)">
                    <button onclick="changeQty(<?= $book['id'] ?>, 1)">+</button>
                </td>
                <td>$<span id="price-<?= $book['id'] ?>"><?= number_format($book['price'], 2) ?></span></td>
                <td>$<span id="subtotal-<?= $book['id'] ?>"><?= number_format($book['subtotal'], 2) ?></span></td>
                <td><a href="cart.php?remove=<?= $book['id'] ?>" class="cart-remove">Remove</a></td>
            </tr>
        <?php endforeach; ?>
        <tr>
            <td colspan="4"><strong>Total:</strong></td>
            <td>$<span id="cart-total"><?= number_format($total, 2) ?></span></td>
            <td colspan="2"></td>
        </tr>
    </table>
    <br>
    <a href="checkout.php" class="checkout-link">Proceed to Checkout</a>
<?php endif; ?>
<script>
function changeQty(id, delta) {
    const input = document.getElementById('qty-' + id);
    let newQty = parseInt(input.value) + delta;
    if (newQty >= 1 && newQty <= 99) {
        updateQty(id, newQty);
    }
}
let debounceTimers = {};

function setQty(id) {
    const input = document.getElementById('qty-' + id);
    let newQty = parseInt(input.value);

    clearTimeout(debounceTimers[id]);
    debounceTimers[id] = setTimeout(() => {
        if (!isNaN(newQty) && newQty >= 1 && newQty <= 99) {
            updateQty(id, newQty);
        } else {
            input.value = 1;
            updateQty(id, 1);
        }
    }, 250); // wait 0.5 sec after typing stops
}
function updateQty(id, newQty) {
    if (newQty < 1 || newQty > 99) return;

    fetch('cart.php?update=1&id=' + id + '&qty=' + newQty)
        .then(() => {
            const price = parseFloat(document.getElementById('price-' + id).textContent);
            const subtotal = price * newQty;
            document.getElementById('subtotal-' + id).textContent = subtotal.toFixed(2);

            // Update displayed quantity
            document.getElementById('qty-' + id).value = newQty;

            // Recalculate total
            let total = 0;
            document.querySelectorAll('[id^="subtotal-"]').forEach(el => {
                total += parseFloat(el.textContent);
            });
            document.getElementById('cart-total').textContent = total.toFixed(2);
        });
}
</script>

<?php require_once '../includes/footer.php'; ?>