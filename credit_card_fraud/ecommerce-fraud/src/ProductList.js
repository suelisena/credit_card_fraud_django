import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaCartPlus } from "react-icons/fa";

function ProductList({ onAddToCart }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // Chama o backend Flask para listar produtos
    axios.get("http://127.0.0.1:5000/products")
      .then(res => setProducts(res.data))
      .catch(err => console.error("Erro ao carregar produtos:", err));
  }, []);

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Produtos disponíveis</h2>
      <div className="row">
        {products.length === 0 ? (
          <p>Nenhum produto encontrado. Verifique se o backend está rodando.</p>
        ) : (
          products.map(product => (
            <div key={product.id} className="col-md-4 mb-3">
              <div className="card shadow-sm">
                <div className="card-body">
                  <h5 className="card-title">{product.name}</h5>
                  <p className="card-text">💲 Preço: R$ {product.price}</p>
                  <p className="card-text">🏬 Loja: {product.merchant}</p>
                  <button
                    className="btn btn-success"
                    onClick={() => onAddToCart(product)}
                  >
                    <FaCartPlus /> Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ProductList;