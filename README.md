# ♟️ DeepChessAcademy (DCA) - Core

Este repositório contém o pipeline de dados MLOps (`dca-core`) para o projeto "DeepChessAcademy".
O objetivo é servir como um plano de estudos prático para as certificações CompTIA DataX (DYO-001) e GCP-MLE.

## 🚀 Módulos do Projeto (Currículo)

* **Módulo 1: O Pipeline de Dados (ETL) & QA**
    * *Status:* **Concluído**
* **Módulo 2: O Valor das Peças (Estatística e EDA)**
    * *Status:* **Concluído**
* **Módulo 3: Vendo o Futuro (ML Clássico)**
    * *Assunto:* Modelos Supervisionados (Regressão Logística), Métricas, Serialização.
    * *Status:* **Em Andamento**
* **Módulo 4: O Tabuleiro "Quente" (Feature Engineering)**
    * *Status:* Pendente
... (etc.)

## 🛠️ Como Executar o Projeto

### 1. Ambiente de Execução (Necessário para ambos)
... (Instruções do venv e requirements.txt) ...

### 2. Módulo 1: Executar o Pipeline de ETL
... (Instrução `python pipeline.py`) ...

### 3. Módulo 2: Executar o Painel de Análise (Dashboard)
... (Instrução `streamlit run dashboard.py`) ...

### 4. Módulo 3: Treinar o Modelo
Isto executa o ciclo de treino e salva o modelo (que é ignorado pelo Git).

1.  **Pré-requisito:** O Módulo 1 deve ter sido executado (o `.csv` deve existir).
2.  Execute o script de treino:
    ```bash
    python train.py
    ```
    * As métricas serão impressas no terminal.
    * O modelo treinado (`model_v1.joblib`) será salvo na pasta `models/`.

## 🧪 Como Executar os Testes (QA do Módulo 1)
... (Instrução `pytest`) ...
