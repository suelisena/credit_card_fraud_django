import React, { useState } from "react";
import axios from "axios";

function Checkout({ product, onClearCart }) {
  const [form, setForm] = useState({
    user_id: 1,
    product_id: product.id,
    amount: product.price,
    transaction_time: 120,
    location: "Los Angeles",
    merchant: product.merchant,
    card_type: "MasterCard"
  });

  const [result, setResult] = useState(null);

  const handleCheckout = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/checkout", form);
      setResult(res.data);
    } catch (err) {
      console.error("Erro no checkout:", err);
    }
  };

  return (
    <div className="card p-3">
      <h3>Checkout</h3>
      <p><strong>Produto:</strong> {product.name}</p>
      <p><strong>Preço:</strong> R$ {product.price}</p>
      <p><strong>Loja:</strong> {product.merchant}</p>

      {/* Campos editáveis */}
      <div className="mb-2">
        <label>Local:</label>
        <input
          type="text"
          value={form.location}
          onChange={e => setForm({ ...form, location: e.target.value })}
          className="form-control"
        />
      </div>

      <div className="mb-2">
        <label>Tipo de Cartão:</label>
        <select
          value={form.card_type}
          onChange={e => setForm({ ...form, card_type: e.target.value })}
          className="form-control"
        >
          <option>Visa</option>
          <option>MasterCard</option>
          <option>Amex</option>
        </select>
      </div>

      <div className="d-flex justify-content-between mt-3">
          <button className="btn btn-success btn-lg" onClick={handleCheckout}> Buy </button>

          <button className="btn btn-danger btn-lg" onClick={onClearCart}>Clear Cart</button>
      </div>

      {result && (
        <div className="mt-3">
          {result.status === "approved" ? (
            <p className="text-success fw-bold fs-5 d-flex align-items-center">
              Compra aprovada (Prob: {result.probability.toFixed(2)})
            </p>
          ) : (
            <p className="text-danger fw-bold fs-5 d-flex align-items-center">
              <span className="me-2">⚠️</span>
              Compra bloqueada (Prob: {result.probability.toFixed(2)})
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default Checkout;