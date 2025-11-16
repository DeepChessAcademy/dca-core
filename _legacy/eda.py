# eda.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import logging
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, RocCurveDisplay

# A configuração do logging é boa, mas será iniciada pelo dashboard
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def carregar_e_limpar_dados(caminho_csv):
    """
    Carrega o CSV, limpa os dados e cria as features base do Módulo 2.
    """
    logging.info(f"Carregando dados de {caminho_csv}...")
    
    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        logging.error(f"ERRO: Ficheiro CSV não encontrado em '{caminho_csv}'.")
        return None
    except Exception as e:
        logging.error(f"Erro ao carregar CSV: {e}")
        return None

    # --- LIMPEZA DE DADOS (CompTIA 4.4) ---
    logging.info("Iniciando limpeza de dados...")
    df['rating_brancas'] = pd.to_numeric(df['rating_brancas'], errors='coerce')
    df['rating_pretas'] = pd.to_numeric(df['rating_pretas'], errors='coerce')
    df['total_lances'] = pd.to_numeric(df['total_lances'], errors='coerce')

    linhas_originais = len(df)
    df.dropna(subset=['rating_brancas', 'rating_pretas', 'total_lances', 'resultado'], inplace=True)
    linhas_limpas = len(df)
    logging.info(f"{linhas_originais - linhas_limpas} linhas com dados inválidos removidas.")
    
    # --- ENGENHARIA DE FEATURE (CompTIA 2.3) ---
    logging.info("Criando features 'Rating_Diferencial' e 'Resultado_Binario'...")
    df['Rating_Diferencial'] = df['rating_brancas'] - df['rating_pretas']
    df['Resultado_Binario'] = np.where(df['resultado'] == '1-0', 1, 0)
    
    # Features adicionais para H7 e H8
    df['abs_Rating_Diferencial'] = df['Rating_Diferencial'].abs()
    df['foi_empate'] = np.where(df['resultado'] == '1/2-1/2', 1, 0)

    logging.info("Dados prontos para análise.")
    return df

# --- Funções das Hipóteses ---

def testar_hipotese_1(df):
    """
    H1: O rating realmente importa? (t-Test)
    Testa se a média do Rating_Diferencial dos vencedores é > 0.
    """
    logging.info("Testando Hipótese 1...")
    vencedores = df[df['Resultado_Binario'] == 1]['Rating_Diferencial']
    
    # t-Test de uma amostra (CompTIA 1.1)
    t_stat, p_value = stats.ttest_1samp(vencedores, 0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(vencedores, bins=50, kde=True, ax=ax, label="Dist. do Rating_Diferencial (Vencedores)")
    ax.axvline(vencedores.mean(), color='red', linestyle='--', label=f'Média: {vencedores.mean():.2f}')
    ax.set_title('H1: Relevância do Rating (t-Test)', fontsize=16)
    ax.set_xlabel('Diferença de Rating')
    ax.legend()
    # Adiciona o resultado do t-test ao gráfico
    ax.text(0.05, 0.9, f't-statistic: {t_stat:.2f}\np-value: {p_value:.2e}', 
            transform=ax.transAxes, fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    return fig

def testar_hipotese_2(df):
    """
    H2: Os ratings individuais são redundantes? (Heatmap)
    Mostra a Multicolinearidade (CompTIA 2.2).
    """
    logging.info("Testando Hipótese 2...")
    cols = ['rating_brancas', 'rating_pretas', 'Rating_Diferencial', 'total_lances', 'Resultado_Binario']
    corr_matrix = df[cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title('H2: Heatmap de Correlação (Multicolinearidade)', fontsize=16)
    
    return fig

def testar_hipotese_3(df):
    """
    H3: A distribuição do matchmaking é 'Normal' e justa?
    """
    logging.info("Testando Hipótese 3...")
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.histplot(df['Rating_Diferencial'], bins=100, kde=True, color='blue', ax=ax)
    
    media = df['Rating_Diferencial'].mean()
    ax.axvline(media, color='red', linestyle='--', label=f'Média: {media:.2f}')
    
    ax.set_title('Hipótese 3: Distribuição do Matchmaking (Rating Brancas - Pretas)', fontsize=16)
    ax.set_xlabel('Diferença de Rating')
    ax.set_ylabel('Frequência de Jogos')
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    return fig

def testar_hipotese_4(df):
    """
    H4: É possível prever a vitória só com o rating? (Regressão Logística)
    (CompTIA 3.2)
    """
    logging.info("Testando Hipótese 4...")
    X = df[['Rating_Diferencial']]
    y = df['Resultado_Binario']
    
    # Dividir os dados
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Treinar o modelo
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Criar visualização (Matriz de Confusão e Curva ROC)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Matriz de Confusão
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', ax=ax1, cmap='Blues')
    ax1.set_title(f'H4: Matriz de Confusão\nAcurácia: {accuracy:.2%}')
    ax1.set_xlabel('Previsto')
    ax1.set_ylabel('Real')
    
    # Curva ROC
    RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax2)
    ax2.set_title('H4: Curva ROC')
    
    return fig

def testar_hipotese_5(df):
    """
    H5: A vantagem das Brancas é real?
    Testa a taxa de vitória das Brancas em jogos equilibrados.
    """
    logging.info("Testando Hipótese 5...")
    # Filtra por jogos "equilibrados"
    df_filtrado = df[df['abs_Rating_Diferencial'] < 50]
    
    if len(df_filtrado) < 30: # Amostra muito pequena para t-test
        logging.warning("Amostra de jogos equilibrados muito pequena para H5.")
        return plt.figure() # Retorna figura vazia

    taxa_vitoria_brancas = df_filtrado['Resultado_Binario'].mean()
    
    # t-Test vs 50% (0.5) (CompTIA 1.1)
    t_stat, p_value = stats.ttest_1samp(df_filtrado['Resultado_Binario'], 0.5)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x=['Esperada (Nula)', 'Observada (Brancas)'], 
        y=[0.5, taxa_vitoria_brancas], 
        ax=ax,
        palette=['grey', 'green']
    )
    ax.set_ylim(0, 1)
    ax.set_title('H5: Taxa de Vitória das Brancas (Jogos Equilibrados)')
    ax.set_ylabel('Taxa de Vitória')
    ax.text(0.5, 0.7, f'p-value: {p_value:.3e}', 
            horizontalalignment='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    return fig

def testar_hipotese_6(df):
    """
    H6: Jogos desiguais terminam mais rápido? (Correlação)
    (CompTIA 1.1)
    """
    logging.info("Testando Hipótese 6...")
    # Correlação de Pearson
    correlacao = df['abs_Rating_Diferencial'].corr(df['total_lances'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Usar .sample() para evitar overplotting (muitos pontos)
    # Usar 10000 pontos para uma boa visualização
    df_sample = df.sample(min(len(df), 10000))
    
    sns.regplot(
        data=df_sample,
        x='abs_Rating_Diferencial', 
        y='total_lances', 
        ax=ax,
        scatter_kws={'alpha':0.1}, # Pontos transparentes
        line_kws={'color':'red'}   # Linha de regressão
    )
    ax.set_title('H6: Diferença de Rating vs. Duração do Jogo', fontsize=16)
    ax.set_xlabel('Diferença Absoluta de Rating')
    ax.set_ylabel('Total de Lances')
    ax.text(0.05, 0.9, f'Correlação (Pearson): {correlacao:.3f}', 
            transform=ax.transAxes, fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
    return fig

def testar_hipotese_7(df):
    """
    H7: Vitórias 'cansadas' dependem menos do rating? (Box Plot)
    (CompTIA 2.1)
    """
    logging.info("Testando Hipótese 7...")
    # Criar categorias de duração (quartis)
    df['Duracao_Jogo'] = pd.qcut(df['total_lances'], 
                                q=4, 
                                labels=['Curto', 'Médio', 'Longo', 'Muito Longo'])
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.boxplot(data=df, x='Duracao_Jogo', y='Rating_Diferencial', ax=ax)
    ax.set_title('H7: Rating vs. Duração da Vitória', fontsize=16)
    ax.set_xlabel('Duração do Jogo (Quartis)')
    ax.set_ylabel('Diferença de Rating')
    
    return fig

def testar_hipotese_8(df):
    """
    H8: Ratings parecidos tendem ao empate? (Gráfico de Barras)
    (CompTIA 2.1)
    """
    logging.info("Testando Hipótese 8...")
    # Criar faixas (bins) de diferença de rating
    bins = [0, 50, 100, 150, 200, 300, 500, df['abs_Rating_Diferencial'].max()]
    labels = ['0-50', '51-100', '101-150', '151-200', '201-300', '301-500', '500+']
    
    df['Faixa_Rating'] = pd.cut(df['abs_Rating_Diferencial'], 
                              bins=bins, 
                              labels=labels, 
                              right=False)
    
    # Calcular a taxa de empate por faixa
    taxa_empate = df.groupby('Faixa_Rating', observed=True)['foi_empate'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=taxa_empate, x='Faixa_Rating', y='foi_empate', ax=ax, palette='viridis')
    ax.set_title('H8: Taxa de Empate vs. Diferença de Rating', fontsize=16)
    ax.set_xlabel('Faixa de Diferença Absoluta de Rating')
    ax.set_ylabel('Taxa de Empate (0.0 a 1.0)')
    
    return fig
