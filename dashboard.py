# dashboard.py
import streamlit as st
import eda # O nosso módulo de EDA
import logging

# --- Configuração da Página ---
st.set_page_config(layout="wide") 

# --- Constantes ---
CSV_PATH = 'data/processed/pipeline_output-00000-of-00001.csv' # CONFIRME O NOME

# --- Carregamento de Dados (com cache) ---
@st.cache_data
def carregar_dados():
    logging.info("Cache do Streamlit vazio. Carregando dados...")
    df = eda.carregar_e_limpar_dados(CSV_PATH)
    return df

df_jogos = carregar_dados()

# --- 1. O CONTROLO NA SIDEBAR (Barra Lateral) ---
st.sidebar.title("♟️ DeepChessAcademy")
st.sidebar.markdown("Módulo 2: Análise de Hipóteses")

opcoes_analise = [
    "--- Selecione uma análise ---",
    "H1: Relevância do Rating (t-Test)",
    "H2: Redundância (Heatmap)",
    "H3: Matchmaking (Distribuição)",
    "H4: Preditividade (Regressão)",
    "H5: Vantagem das Brancas",
    "H6: Jogo Rápido (Correlação)",
    "H7: Vitória Cansada (Box Plot)",
    "H8: Tensão do Empate (Barras)",
    "Ver Amostra dos Dados"
]
escolha = st.sidebar.selectbox("Testador de Hipóteses:", opcoes_analise)

# --- 2. Funções de Renderização (com Cache) ---
# Usar cache para os gráficos acelera muito o dashboard
@st.cache_data
def render_h1(df): return eda.testar_hipotese_1(df)

@st.cache_data
def render_h2(df): return eda.testar_hipotese_2(df)

@st.cache_data
def render_h3(df): return eda.testar_hipotese_3(df)

@st.cache_data
def render_h4(df): return eda.testar_hipotese_4(df)

@st.cache_data
def render_h5(df): return eda.testar_hipotese_5(df)

@st.cache_data
def render_h6(df): return eda.testar_hipotese_6(df)

@st.cache_data
def render_h7(df): return eda.testar_hipotese_7(df)

@st.cache_data
def render_h8(df): return eda.testar_hipotese_8(df)


# --- 3. O DISPLAY PRINCIPAL (Renderização Condicional) ---
if df_jogos is None:
    st.error(f"Erro ao carregar os dados. Verifique o caminho: {CSV_PATH}")
else:
    if escolha == "--- Selecione uma análise ---":
        st.title("Painel de Análise (Módulo 2)")
        st.markdown("Bem-vindo ao painel de Análise Exploratória de Dados (EDA).")
        st.markdown("Use o **menu na barra lateral esquerda** para selecionar qual das 8 hipóteses você deseja testar.")

    elif escolha == "H1: Relevância do Rating (t-Test)":
        st.header("Hipótese 1: O rating realmente importa?")
        st.markdown("Testamos (com um t-Test) se a média do `Rating_Diferencial` dos vencedores é estatisticamente maior que zero.")
        fig = render_h1(df_jogos)
        st.pyplot(fig)

    elif escolha == "H2: Redundância (Heatmap)":
        st.header("Hipótesese 2: Os ratings individuais são redundantes?")
        st.markdown("Este Heatmap de Correlação mostra a **Multicolinearidade**. Note como `rating_brancas` e `rating_pretas` são altamente correlacionados (próximo de 1.0), justificando a criação da feature `Rating_Diferencial`.")
        fig = render_h2(df_jogos)
        st.pyplot(fig)

    elif escolha == "H3: Matchmaking (Distribuição)":
        st.header("Hipótese 3: O Matchmaking do Lichess é justo?")
        st.markdown("A distribuição do `Rating_Diferencial` deve ser uma curva 'normal' (sino) centrada perto de zero, o que indica um pareamento justo.")
        fig = render_h3(df_jogos)
        st.pyplot(fig)

    elif escolha == "H4: Preditividade (Regressão)":
        st.header("Hipótese 4: É possível prever a vitória só com o rating?")
        st.markdown("Treinamos um modelo de Regressão Logística. A Matriz de Confusão mostra os acertos/erros e a Curva ROC mostra o poder preditivo (quanto mais perto de 1, melhor).")
        fig = render_h4(df_jogos)
        st.pyplot(fig)
        
    elif escolha == "H5: Vantagem das Brancas":
        st.header("Hipótese 5: A vantagem das Brancas é real?")
        st.markdown("Filtramos apenas por jogos 'equilibrados' (|Rating| < 50) e comparamos a taxa de vitória observada das Brancas contra a esperada (50%). O p-value nos diz se a diferença é estatisticamente significativa.")
        fig = render_h5(df_jogos)
        st.pyplot(fig)

    elif escolha == "H6: Jogo Rápido (Correlação)":
        st.header("Hipótese 6: Jogos desiguais terminam mais rápido?")
        st.markdown("Este gráfico mostra a correlação entre a `Diferença Absoluta de Rating` e o `Total de Lances`. Uma correlação negativa (linha vermelha descendente) confirma a hipótese.")
        fig = render_h6(df_jogos)
        st.pyplot(fig)

    elif escolha == "H7: Vitória Cansada (Box Plot)":
        st.header("Hipótese 7: Vitórias 'cansadas' dependem menos do rating?")
        st.markdown("Este Box Plot mostra a distribuição do `Rating_Diferencial` por 'quartis' de duração do jogo. Se as 'caixas' de jogos longos estiverem mais próximas de zero, a hipótese é suportada.")
        fig = render_h7(df_jogos)
        st.pyplot(fig)
        
    elif escolha == "H8: Tensão do Empate (Barras)":
        st.header("Hipótese 8: Ratings parecidos tendem ao empate?")
        st.markdown("Calculamos a 'taxa de empate' para diferentes faixas de diferença de rating. Como esperado, quanto menor a diferença ('0-50'), maior a probabilidade de empate.")
        fig = render_h8(df_jogos)
        st.pyplot(fig)

    elif escolha == "Ver Amostra dos Dados":
        st.header("Amostra dos Dados Limpos (Módulo 1)")
        st.markdown("Uma amostra dos dados após a limpeza e engenharia de features (Módulo 2).")
        st.dataframe(df_jogos)