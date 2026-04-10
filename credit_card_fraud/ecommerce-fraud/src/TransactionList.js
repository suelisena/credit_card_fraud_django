import React, { useState, useEffect } from "react";
import axios from "axios";

function TransactionList() {
  const [transactions, setTransactions] = useState([]);
  const [userId, setUserId] = useState("");

  useEffect(() => {
    const url = userId
      ? `http://127.0.0.1:5000/transactions?user_id=${userId}`
      : "http://127.0.0.1:5000/transactions";

    axios.get(url)
      .then(res => setTransactions(res.data))
      .catch(err => console.error("Erro ao carregar transações:", err));
  }, [userId]);

  return (
    <div className="container mt-5">
      <h2>Histórico de Transações</h2>

      <div className="mb-3">
        <label>Filtrar por usuário:</label>
        <input
          type="number"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          className="form-control"
          placeholder="Digite o ID do usuário"
        />
      </div>

      <table className="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>User</th>
            <th>Produto</th>
            <th>Valor</th>
            <th>Local</th>
            <th>Loja</th>
            <th>Cartão</th>
            <th>Fraude</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(tx => (
            <tr key={tx.id}>
              <td>{tx.id}</td>
              <td>{tx.user_id}</td>
              <td>{tx.product_id}</td>
              <td>R$ {tx.amount}</td>
              <td>{tx.location}</td>
              <td>{tx.merchant}</td>
              <td>{tx.card_type}</td>
              <td>{tx.is_fraud === 1 ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionList;