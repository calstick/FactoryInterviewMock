const state = {
  token: null,
  customerName: null,
  products: [],
  cart: {}, // product_id -> { product, quantity }
};

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers["Authorization"] = `Bearer ${state.token}`;
  const res = await fetch(path, { ...options, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.status === 204 ? null : res.json();
}

async function loadProducts() {
  state.products = await api("/products");
  renderProducts();
}

function renderProducts() {
  const grid = $("products");
  grid.innerHTML = "";
  for (const p of state.products) {
    const card = document.createElement("div");
    card.className = "product-card";
    const outOfStock = p.stock <= 0;
    card.innerHTML = `
      <span class="category">${p.category}</span>
      <h4>${p.name}</h4>
      <span class="price">$${p.price.toFixed(2)}</span>
      <span class="stock ${outOfStock ? "out" : ""}">${outOfStock ? "Out of stock" : p.stock + " in stock"}</span>
    `;
    const clamp = (v) => Math.max(1, Math.min(99, Number.isFinite(v) ? v : 1));

    const stepper = document.createElement("div");
    stepper.className = "stepper";
    const minus = document.createElement("button");
    minus.className = "step";
    minus.textContent = "\u2212";
    const qtyInput = document.createElement("input");
    qtyInput.className = "qty-input";
    qtyInput.type = "number";
    qtyInput.min = "1";
    qtyInput.max = "99";
    qtyInput.value = "1";
    const plus = document.createElement("button");
    plus.className = "step";
    plus.textContent = "+";
    minus.onclick = () => { qtyInput.value = clamp(parseInt(qtyInput.value, 10) - 1); };
    plus.onclick = () => { qtyInput.value = clamp(parseInt(qtyInput.value, 10) + 1); };
    qtyInput.onchange = () => { qtyInput.value = clamp(parseInt(qtyInput.value, 10)); };
    stepper.append(minus, qtyInput, plus);

    const btn = document.createElement("button");
    btn.className = "btn add";
    btn.textContent = "Add to cart";
    btn.disabled = outOfStock;
    btn.onclick = () => addToCart(p, clamp(parseInt(qtyInput.value, 10)));

    if (!outOfStock) card.appendChild(stepper);
    card.appendChild(btn);
    grid.appendChild(card);
  }
}

function addToCart(product, quantity = 1) {
  const entry = state.cart[product.id] || { product, quantity: 0 };
  entry.quantity += quantity;
  state.cart[product.id] = entry;
  refreshCart();
}

async function refreshCart() {
  const container = $("cart-items");
  const ids = Object.keys(state.cart);
  if (ids.length === 0) {
    container.innerHTML = '<p class="muted">Your cart is empty.</p>';
    $("totals").innerHTML = "";
    $("checkout-btn").disabled = true;
    return;
  }
  container.innerHTML = "";
  for (const id of ids) {
    const { product, quantity } = state.cart[id];
    const row = document.createElement("div");
    row.className = "cart-row";
    row.innerHTML = `<span>${product.name}</span><span class="qty">x${quantity}</span>`;
    container.appendChild(row);
  }

  const items = ids.map((id) => ({ product_id: Number(id), quantity: state.cart[id].quantity }));
  try {
    const preview = await api("/cart/preview", { method: "POST", body: JSON.stringify({ items }) });
    $("totals").innerHTML = `
      <div class="row"><span>Subtotal</span><span>$${preview.subtotal.toFixed(2)}</span></div>
      <div class="row"><span>Discount</span><span class="disc">-$${preview.discount.toFixed(2)}</span></div>
      <div class="row"><span>Tax</span><span>$${preview.tax.toFixed(2)}</span></div>
      <div class="row grand"><span>Total</span><span>$${preview.total.toFixed(2)}</span></div>
    `;
  } catch (e) {
    $("totals").innerHTML = `<p class="message error">${e.message}</p>`;
  }
  $("checkout-btn").disabled = !state.token;
}

async function checkout() {
  const items = Object.keys(state.cart).map((id) => ({
    product_id: Number(id),
    quantity: state.cart[id].quantity,
  }));
  try {
    const order = await api("/orders", { method: "POST", body: JSON.stringify({ items }) });
    setMessage(`Order #${order.id} placed · total $${order.total.toFixed(2)}`, "success");
    state.cart = {};
    await loadProducts();
    refreshCart();
  } catch (e) {
    setMessage(e.message, "error");
  }
}

function setMessage(text, kind) {
  const el = $("message");
  el.textContent = text;
  el.className = `message ${kind || ""}`;
}

async function login() {
  $("login-error").textContent = "";
  try {
    const res = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email: $("email").value, password: $("password").value }),
    });
    state.token = res.token;
    state.customerName = res.name;
    $("session-status").textContent = `Signed in as ${res.name}`;
    $("session-status").classList.remove("muted");
    $("login-btn").style.display = "none";
    $("login-modal").classList.add("hidden");
    refreshCart();
  } catch (e) {
    $("login-error").textContent = e.message;
  }
}

$("login-btn").onclick = () => $("login-modal").classList.remove("hidden");
$("login-cancel").onclick = () => $("login-modal").classList.add("hidden");
$("login-submit").onclick = login;
$("checkout-btn").onclick = checkout;

loadProducts();
