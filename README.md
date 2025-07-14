# 🎯 Projeto BigQuery

Projeto de realização de PoC de criação de processo de configuração, ingestão e consumo de uma fonte de dados no BigQuery.

# 📊 Documentação do Pipeline de Dados: Ingestão no GCP e Visualização com Power BI

Este repositório descreve a **Fase 1 de um pipeline de dados completo**, focado na ingestão e disponibilização de dados no Google Cloud Platform (GCP), com posterior uso no Power BI para visualização.

---

## 📌 Fase 1: Obtenção e Disponibilização dos Dados (API + Cloud Storage)

Nesta etapa, o objetivo é:

* Obter os dados de um arquivo CSV local
* Criar uma API com **FastAPI** que expõe esses dados no endpoint `/veiculos`
* Realizar o upload do arquivo para o **Cloud Storage (GCP)**
* Automatizar o processo de ingestão com **Cloud Run + Cloud Functions**

> ⚠️ **Pré-requisitos**:
>
> * Realize as configurações de ambiente e permissões descritas abaixo.
> * Mantenha os arquivos organizados por função (API e função de carga).
> * Utilize a ferramenta de debug do VS Code para validações locais.

---

## ☁️ Provisionamento no Google Cloud Platform (GCP)

### 1. Criar uma conta gratuita

Acesse: [https://cloud.google.com](https://cloud.google.com)
→ A conta gratuita oferece **US\$ 300 em créditos por 90 dias**

### 2. Criar um projeto

Nome sugerido: `bigquery-ingestion`

### 3. Criar um bucket no Cloud Storage

* Acesse: [Console do GCP – Storage](https://console.cloud.google.com/storage)
* Nome do bucket: `meu-bucket-dados-poc`

### 4. Criar uma conta de serviço com chave JSON

* Acesse: [Contas de Serviço – IAM](https://console.cloud.google.com/iam-admin/serviceaccounts)
* Nome: `servicos-poc`
* Permissão: `Storage Object Admin` (`roles/storage.objectAdmin`)
* Gere e **baixe a chave JSON**
* Mova o arquivo para a pasta do projeto

---

## ⚙️ Configuração do Ambiente de Desenvolvimento

### 1. Instalar Python 3.10+ no macOS

➡️ [Download Python para macOS](https://www.python.org/downloads/mac-osx/)

### 2. Instalar Visual Studio Code

➡️ [Download VS Code](https://code.visualstudio.com/)
Extensões recomendadas: **Python**, **Pylance**

### 3. Instalar dependências

```bash
pip install fastapi uvicorn pandas google-cloud-storage requests
```

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

## 🚀 Publicação da API no Cloud Run

### Estrutura básica do repositório:

```
📁 api/
├── main.py
├── requirements.txt
└── veiculos_mais_vendidos_2024_completo.csv
```

### Passo a passo realizado:

1. Acessar o Console do GCP > Cloud Run > Criar Serviço
2. Selecionar a origem do código como GitHub (opção de CI/CD)
3. Escolher a branch `main` e tipo de build `buildpacks`
4. Informar a linguagem: Python 3.10
5. Deixar o ponto de entrada em branco (FastAPI detecta automaticamente)
6. Habilitar acesso não autenticado
7. Implantar o serviço e copiar o endpoint gerado

---

## 🔁 Script de Ingestão Automática via Cloud Run (Editor In-line)

### 🔹 Código da função — `main.py`

```python
import functions_framework
import pandas as pd
import requests
from google.cloud import storage

NOME_BUCKET = "meu-bucket-dados-poc"
DESTINO_NO_BUCKET = "documento_poc/veiculos_mais_vendidos_2024_completo.csv"
URL_API_VEICULOS = "https://sua-api-url.a.run.app/veiculos"  # substitua pela URL real

@functions_framework.http
def carga_csv_para_gcs(request):
    try:
        response = requests.get(URL_API_VEICULOS)
        response.raise_for_status()
        dados = response.json()

        df = pd.DataFrame(dados)
        caminho_tmp = "/tmp/veiculos_mais_vendidos.csv"
        df.to_csv(caminho_tmp, index=False)

        client = storage.Client()
        bucket = client.bucket(NOME_BUCKET)
        blob = bucket.blob(DESTINO_NO_BUCKET)
        blob.upload_from_filename(caminho_tmp)

        return {"status": "sucesso", "mensagem": f"Arquivo enviado para gs://{NOME_BUCKET}/{DESTINO_NO_BUCKET}"}

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
```

### 🔹 `requirements.txt`

```
functions-framework
pandas
requests
google-cloud-storage
```

### Passo a passo realizado para o script de carga:

1. Acessar Cloud Run > Criar serviço > opção “Escrever função”
2. Inserir o nome `carga-poc`, selecionar a região `southamerica-east1`
3. Escolher linguagem Python 3.10
4. Inserir os arquivos `main.py` e `requirements.txt` manualmente
5. No campo “Ponto de entrada da função”, digitar `carga_csv_para_gcs`
6. Habilitar acesso não autenticado
7. Implantar o serviço
8. Testar a função acessando o endpoint via navegador ou curl

---

## ✅ Status da Fase 1

* ✅ API funcional com dados do CSV publicada no Cloud Run
* ✅ Upload automatizado com função em Cloud Run
* ✅ Dados disponíveis no Cloud Storage

---

➡️ **Com o arquivo `veiculos_mais_vendidos_2024_completo.csv` armazenado automaticamente no bucket `meu-bucket-dados-poc`, a Fase 1 está concluída.**

Próxima etapa: **ingestão no BigQuery e visualização no Power BI.**
