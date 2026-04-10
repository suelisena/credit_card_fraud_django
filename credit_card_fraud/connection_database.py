import mysql.connector
import pandas as pd

# conexao com o banco de dados

#def get_transactions():

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123', 
    database='fraud_card')

# Extrair dados para o DataFrame

df = pd.read_sql('SELECT * FROM transactions',conn)
conn.close()

df.to_csv('transactions.csv', index=False)
print("Dados exportados para transactions.csv com sucesso!")


    #print(df.head())
    #return df

#if __name__ == "__main__":
    #data = get_transactions()
    #print(data.head())



   
