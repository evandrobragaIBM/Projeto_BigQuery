import requests
import pandas as pd
from google.cloud import storage
from datetime import datetime
import os

# Configurações
API_URL = "https://projeto-bigquery-986909343514.southamerica-east1.run.app/veiculos"  # Substitua aqui
NOME_BUCKET = "meu-bucket-dados-poc"
DESTINO_NO_BUCKET = f"documento_poc/veiculos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def ingestar_dados(request):
    try:
        # 1. Chama a API
        response = requests.get(API_URL)
        response.raise_for_status()
        dados = response.json()

        # 2. Converte para DataFrame
        df = pd.DataFrame(dados)

        # 3. Salva localmente
        temp_path = "/tmp/veiculos.csv"
        df.to_csv(temp_path, index=False)

        # 4. Envia ao Cloud Storage
        client = storage.Client()
        bucket = client.bucket(NOME_BUCKET)
        blob = bucket.blob(DESTINO_NO_BUCKET)
        blob.upload_from_filename(temp_path)

        return f"✔️ Dados enviados para gs://{NOME_BUCKET}/{DESTINO_NO_BUCKET}", 200

    except Exception as e:
        return f"❌ Erro: {str(e)}", 500
