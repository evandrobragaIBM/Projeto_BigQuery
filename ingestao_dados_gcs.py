from google.cloud import storage

# Caminho do arquivo CSV local
CAMINHO_LOCAL = "/Users/evandrobraga/Desktop/Projeto Ingestion_Query/veiculos_mais_vendidos_2024_completo.csv"

# Nome do bucket já criado no seu projeto
NOME_BUCKET = "meu-bucket-dados-poc"
# Caminho no bucket onde o arquivo será armazenado
DESTINO_NO_BUCKET = "Documento PoC/veiculos_mais_vendidos_2024_completo.csv"

def upload_csv_para_bucket():
    # Cria cliente autenticado
    client = storage.Client()
    
    # Referência ao bucket
    bucket = client.bucket(NOME_BUCKET)
    
    # Cria referência ao arquivo (blob) de destino
    blob = bucket.blob(DESTINO_NO_BUCKET)
    
    # Faz o upload
    blob.upload_from_filename(CAMINHO_LOCAL)
    
    print(f"✔️ Upload concluído: gs://{NOME_BUCKET}/{DESTINO_NO_BUCKET}")

if __name__ == "__main__":
    upload_csv_para_bucket()
