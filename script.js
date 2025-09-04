const cartItemsContainer = document.getElementById("cart-items");
const cartTotalEl = document.getElementById("cart-total");
const checkoutBtn = document.getElementById("checkout");

let cart = JSON.parse(localStorage.getItem("cart")) || [];

function renderCart() {
  cartItemsContainer.innerHTML = "";
  if (cart.length === 0) {
    cartItemsContainer.textContent = "Belum ada item";
  } else {
    cart.forEach((item, index) => {
      const div = document.createElement("div");
      div.textContent = `${item.name} x${item.qty} - Rp${
        item.price * item.qty
      }`;
      const removeBtn = document.createElement("button");
      removeBtn.textContent = "Hapus";
      removeBtn.style.marginLeft = "10px";
      removeBtn.onclick = () => removeItem(index);
      div.appendChild(removeBtn);
      cartItemsContainer.appendChild(div);
    });
  }
  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  cartTotalEl.textContent = total.toLocaleString();
  localStorage.setItem("cart", JSON.stringify(cart));
}

function removeItem(index) {
  cart.splice(index, 1);
  renderCart();
}

document.querySelectorAll(".add-cart").forEach((btn) => {
  btn.addEventListener("click", () => {
    const name = btn.dataset.name;
    const price = parseInt(btn.dataset.price);
    const existing = cart.find((i) => i.name === name);
    if (existing) {
      existing.qty++;
    } else {
      cart.push({ name, price, qty: 1 });
    }
    renderCart();
  });
});

// === Checkout Kirim ke Bot via Flask ===
checkoutBtn.addEventListener("click", () => {
  if (cart.length === 0) return alert("Keranjang masih kosong!");
  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);

  fetch("http://localhost:5000/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items: cart, total: total }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert("Checkout berhasil! Pesanan terkirim ke Discord.");
      cart = [];
      renderCart();
    })
    .catch((err) => alert("Gagal checkout: " + err));
});

renderCart();
