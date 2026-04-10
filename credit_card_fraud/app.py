from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Conexão com MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='fraud_card'
)
cursor = db.cursor(dictionary=True)

# Carregar modelo, scaler e colunas
model = joblib.load('fraud_model.pkl')
scaler = joblib.load('scaler.pkl')
X_columns = joblib.load('X_columns.pkl')

def predict_transaction_with_prob(amount, transaction_time, location, merchant, card_type):
    new_transaction = pd.DataFrame([[amount, transaction_time, location, merchant, card_type]],
                                   columns=['amount', 'transaction_time', 'location', 'merchant', 'card_type'])
    new_transaction = pd.get_dummies(new_transaction, columns=['location', 'merchant', 'card_type'], drop_first=True)
    new_transaction = new_transaction.reindex(columns=X_columns, fill_value=0)
    new_transaction[['amount', 'transaction_time']] = scaler.transform(new_transaction[['amount', 'transaction_time']])
    prob = model.predict_proba(new_transaction)[0][1]
    prediction = model.predict(new_transaction)[0]
    return bool(prediction), prob

# ✅ Rota para listar produtos
@app.route("/products", methods=["GET"])
def get_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

# ✅ Rota para checkout
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    user_id = data["user_id"]
    product_id = data["product_id"]
    amount = float(data["amount"])
    transaction_time = int(data["transaction_time"])
    location = data["location"]
    merchant = data["merchant"]
    card_type = data["card_type"]

    # Predição de fraude
    fraud, prob = predict_transaction_with_prob(amount, transaction_time, location, merchant, card_type)

    # Inserir transação no banco
    cursor.execute("""
        INSERT INTO transactions (user_id, product_id, amount, transaction_time, location, merchant, card_type, is_fraud)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, product_id, amount, transaction_time, location, merchant, card_type, int(fraud)))
    db.commit()

    if fraud and prob > 0.7:
        return jsonify({"status": "blocked", "probability": prob})
    else:
        return jsonify({"status": "approved", "probability": prob})

# ✅ Rota para listar transações
@app.route("/transactions", methods=["GET"])
def get_transactions():
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    return jsonify(transactions)

# ✅ Rota para listar usuários
@app.route("/users", methods=["GET"])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route("/users/<int:user_id>/transactions", methods=["GET"])
def get_user_transactions():
    user_id = request.args.get("user_id")  # pega ?user_id=1 da URL
    if user_id:
        cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    else:
        cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(debug=True)