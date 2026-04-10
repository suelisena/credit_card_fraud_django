import React, { useState } from "react";
import ProductList from "./ProductList";
import Checkout from "./Checkout";
import TransactionList from "./TransactionList";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [selectedProduct, setSelectedProduct] = useState(null);

  // Função para limpar o carrinho
  const clearCart = () => {
    setSelectedProduct(null);
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">E-commerce Fraud Detection</h1>

      {/* Vitrine de produtos */}
      <ProductList onAddToCart={setSelectedProduct} />

      {/* Checkout com produto selecionado */}
      {selectedProduct && (
        <div className="mt-5">
          <Checkout product={selectedProduct} onClearCart={clearCart} />
        </div>
      )}

      {/* Histórico de transações */}
      <div className="mt-5">
        <TransactionList />
      </div>
    </div>
  );
}

export default App;
