from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

# Caminho do arquivo CSV
CSV_PATH = "/Users/evandrobraga/Desktop/Projeto Ingestion_Query/veiculos_mais_vendidos_2024_completo.csv"

@app.get("/")
def home():
    return {"mensagem": "API está rodando. Acesse /veiculos para ver os dados."}

@app.get("/veiculos")
def listar_veiculos():
    if not os.path.exists(CSV_PATH):
        return {"erro": "Arquivo CSV não encontrado."}
    
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient="records")
