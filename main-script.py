import functions_framework
import pandas as pd
import requests
from google.cloud import storage

# Nome do bucket e caminho destino
NOME_BUCKET = "seu-bucket"
DESTINO_NO_BUCKET = "pasta-exemplo/veiculos_mais_vendidos_2024_completo.csv"

# Endpoint da sua API FastAPI no Cloud Run
URL_API_VEICULOS = "https://sua-url/veiculos"

@functions_framework.http
def carga_csv_para_gcs(request):
    try:
        # 1. Requisição para API de veículos
        response = requests.get(URL_API_VEICULOS)
        response.raise_for_status()
        dados = response.json()

        # 2. Gravar CSV temporário
        df = pd.DataFrame(dados)
        caminho_tmp = "/tmp/veiculos_mais_vendidos.csv"
        df.to_csv(caminho_tmp, index=False)

        # 3. Upload para o Cloud Storage
        client = storage.Client()
        bucket = client.bucket(NOME_BUCKET)
        blob = bucket.blob(DESTINO_NO_BUCKET)
        blob.upload_from_filename(caminho_tmp)

        return {"status": "sucesso", "mensagem": f"Arquivo enviado para gs://{NOME_BUCKET}/{DESTINO_NO_BUCKET}"}

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
