# 🎯 Projeto BigQuery
Projeto de realização de PoC de criação de proceso de configuração, ingestão e consumo de uma fonte de dados no BigQuery.

# 📊 Documentação do Pipeline de Dados: Ingestão no GCP e Visualização com Power BI

Este repositório descreve a **Fase 1 de um pipeline de dados completo**, focado na ingestão e disponibilização de dados no Google Cloud Platform (GCP), com posterior uso no Power BI para visualização.

---

## 📌 Fase 1: Obtenção e Disponibilização dos Dados (API + Cloud Storage)

Nesta etapa, o objetivo é:

- Obter os dados de um arquivo CSV local
- Criar uma API com **FastAPI** que expõe esses dados no endpoint `/veiculos`
- Realizar o upload do arquivo para o **Cloud Storage (GCP)** para posterior integração com BigQuery

> ⚠️ **Pré-requisitos**:
> - Realize as configurações de ambiente e permissões descritas abaixo.
> - Mantenha os arquivos na mesma pasta do projeto para melhor funcionamento.
> - Utilize a ferramenta de debug do VS Code para validações locais.

---

## ☁️ Provisionamento no Google Cloud Platform (GCP)

### 1. Criar uma conta gratuita
Acesse: [https://cloud.google.com](https://cloud.google.com)  
→ A conta gratuita oferece **US$ 300 em créditos por 90 dias**

### 2. Criar um projeto
Nome sugerido: `bigquery-ingestion`

### 3. Criar um bucket no Cloud Storage
- Acesse: [Console do GCP – Storage](https://console.cloud.google.com/storage)
- Nome do bucket: `seu-bucket`

### 4. Criar uma conta de serviço com chave JSON
- Acesse: [Contas de Serviço – IAM](https://console.cloud.google.com/iam-admin/serviceaccounts)
- Nome: `servicos-poc`
- Permissão: `Storage Object Admin` (`roles/storage.objectAdmin`)
- Gere e **baixe a chave JSON**
- Mova o arquivo para a pasta do projeto

---

## ⚙️ Configuração do Ambiente de Desenvolvimento

### 1. Instalar Python 3.10+ no macOS
➡️ [Download Python para macOS](https://www.python.org/downloads/mac-osx/)

### 2. Instalar Visual Studio Code
➡️ [Download VS Code](https://code.visualstudio.com/)  
Extensões recomendadas: **Python**, **Pylance**

### 3. Instalar dependências

```bash
pip install fastapi uvicorn pandas google-cloud-storage
```

### IMPORTANTE: pip3 para Mac e sempre utilizar Bash.

---

## 📄 Scripts da Fase 1

### 🔹 API com FastAPI — `main.py`

```python
from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()
CSV_PATH = "veiculos_mais_vendidos_2024_completo.csv"

@app.get("/")
def home():
    return {"mensagem": "API está rodando. Acesse /veiculos para ver os dados."}

@app.get("/veiculos")
def listar_veiculos():
    if not os.path.exists(CSV_PATH):
        return {"erro": "Arquivo CSV não encontrado."}
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient="records")
```

### ▶️ Executar a API no Terminal Bash

```bash
uvicorn main:app --reload
```

---

### 🔹 Script de upload para o GCS — `ingestao_dados_gcs.py`

```python
from google.cloud import storage

# Caminho do arquivo CSV local
CAMINHO_LOCAL = "/Users/seu-user/Desktop/Projeto Ingestion_Query/veiculos_mais_vendidos_2024_completo.csv"

# Nome do bucket já criado no seu projeto
NOME_BUCKET = "seu-bucket" # Adicione o nome do seu bucket criado
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
```

> ⚠️ Antes de rodar esse script, defina a variável de ambiente. Rode o comando junto no terminal:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/seu-user/Desktop/Projeto Ingestion_Query/nome-da-sua-chave.json"
python ingestao_dados_gcs.py
```

---

### 🚧 Possíveis erros e solução

#### Erro:
```
Permission 'storage.objects.create' denied
```

#### Solução:
1. Acesse o bucket no console GCP
2. Vá até a aba **"Permissões"**
3. Clique em **"Conceder acesso"**
4. Informe o **e-mail da conta de serviço** (disponível no JSON)
5. Atribua a permissão: `Storage Object Admin`
6. Salve e tente novamente

---

## ✅ Status da Fase 1

- ✅ API funcional com dados do CSV
- ✅ Upload para o Cloud Storage realizado com sucesso
- ✅ Autenticação via conta de serviço configurada

---

➡️ **Com o arquivo `veiculos_mais_vendidos_2024_completo.csv` armazenado no bucket `seu-bucket`, a Fase 1 está concluída.**

Próxima etapa: **ingestão automatizada no BigQuery e visualização no Power BI.**
