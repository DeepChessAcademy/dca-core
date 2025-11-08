# Changelog

Todo o progresso notável neste projeto será documentado aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Em Andamento] - Módulo 2 (EDA & Dashboard)

### Adicionado
* **Painel de Análise (Dashboard):** Criado `dashboard.py` com `Streamlit` para visualização interativa de dados.
* **Módulo de Análise (`eda.py`):** Refatorado para ser uma biblioteca de funções de análise (carregamento, limpeza, plotagem).
* **Novas Dependências:** Adicionado `streamlit`, `seaborn`, `scipy`, e `scikit-learn` ao `requirements.txt`.
* **Engenharia de Features:** Criadas features `Rating_Diferencial`, `Resultado_Binario`, `abs_Rating_Diferencial` e `foi_empate` no script de limpeza.
* **Testes de Hipótese (H1-H8):** Implementadas todas as 8 funções de análise estatística e visualização no `eda.py`.

### Observação
* **H5 Vazia:** A Hipótese 5 (Vantagem das Brancas) está a retornar um gráfico vazio. A investigação inicial sugere que a amostra de dados de jogos "equilibrados" (`< 50` pontos de diferença) no PGN de teste atual é muito pequena (`< 30` jogos), fazendo com que a "trava de segurança" estatística retorne uma figura vazia. Isto será analisado futuramente.

## [1.0.0] - Módulo 1 (Pipeline ETL Estável) - 2025-11-06

### Adicionado
* Configuração do ambiente local com `Python 3.11` e `venv`.
* Estrutura de pastas profissional (`data/raw`, `data/processed`).
* Pipeline de ETL (`pipeline.py`) usando `Apache Beam` (`DirectRunner`).
* Lógica de parsing (`parser.py`) capaz de processar ficheiros PGN massivos.
* Sistema de logging robusto (`pipeline.log`).
* Configuração de documentação (`LICENSE`, `README.md`, `CHANGELOG.md`).
* Configuração de controlo de versão (`.gitignore`).

### Alterado
* **Refatoração de QA:** A lógica de parsing foi movida de `pipeline.py` para `parser.py` para permitir testes de unidade (baixo acoplamento).

### Corrigido (Estabilidade do Pipeline & QA)
* **(QA) Bug Lógico:** O teste de unidade (`pytest`) falhou, identificando um bug na contagem de lances (`game.ply()`). Lógica em `parser.py` corrigida para `len(list(game.mainline_moves()))`.
* **(Pipeline) `TypeError`:** Substituído `beam.FlatMap` por `beam.ParDo` em `pipeline.py` para corrigir o `TypeError` ao chamar a classe `DoFn` (`ParsePgnFile`).
* **(Pipeline) `DEADLINE_EXCEEDED`:** Aumentado o timeout do Apache Beam DirectRunner para `600s` (`direct_runner_service_checkout_timeout_seconds`) nas `PipelineOptions`, permitindo o processamento de PGNs grandes (ex: 90MB) sem falha de timeout.
