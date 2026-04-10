import joblib
import pandas as pd
import os
from django.conf import settings

BASE_MODEL_DIR = os.path.join(settings.BASE_DIR, 'modelos')

def fazer_predicao_fraude(dados_dict):
    # 1. Carregar artefatos
    modelo = joblib.load(os.path.join(BASE_MODEL_DIR, 'fraud_model.pkl'))
    scaler = joblib.load(os.path.join(BASE_MODEL_DIR, 'scaler.pkl'))
    colunas_treino = joblib.load(os.path.join(BASE_MODEL_DIR, 'X_columns.pkl'))

    # 2. Criar DataFrame com TODAS as colunas do treino zeradas
    df_final = pd.DataFrame(0, index=[0], columns=colunas_treino)

    # 3. Preencher dados vindos do formulário
    df_final['amount'] = float(dados_dict['amount'])
    df_final['transaction_time'] = 0  # Valor padrão

    # 4. Preencher as categorias (One-Hot Encoding manual)
    categorias = {
        'location': dados_dict['location'],
        'merchant': dados_dict['merchant'],
        'card_type': dados_dict['card_type']
    }

    for prefixo, valor in categorias.items():
        coluna_nome = f"{prefixo}_{valor}"
        if coluna_nome in df_final.columns:
            df_final[coluna_nome] = 1

   
    # 5. Escalonar APENAS as colunas que o scaler conhece (amount e transaction_time)
    colunas_numericas = ['amount', 'transaction_time']
    df_final[colunas_numericas] = scaler.transform(df_final[colunas_numericas])

    # 6. Garantir que a ordem das colunas está idêntica ao que o MODELO espera
    df_final = df_final[colunas_treino]

    # 7. Fazer a Predição usando o DataFrame completo
    predicao = modelo.predict(df_final)[0]
    probabilidade = modelo.predict_proba(df_final)[0][1]

    return int(predicao), float(probabilidade)