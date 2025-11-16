# ext_pipeline.py
"""
Pipeline extensor para processamento de PGNs anotados (v2).

Este pipeline:
1. Localiza arquivos PGN em 'data/annotated_pgns/'.
2. Usa o `ext_parser` (v2) para extrair dados (lance + headers).
3. Salva os dados consolidados em 'data/processed/lance_analysis_v2.csv'.
"""

import os
import pandas as pd
from ext_parser import parse_annotated_pgn # Importa do parser v2

# --- Configuração do Sistema de Arquivos Extensor ---
INPUT_DIR = "data/annotated_pgns"
OUTPUT_DIR = "data/processed"
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, "lance_analysis_v2.csv")
# ---------------------------------------------------

def run_annotated_pipeline():
    """
    Executa o pipeline completo de ETL para PGNs anotados.
    """
    print("Iniciando pipeline de análise de lances v2 (ext_pipeline)...")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_moves_data = []
    
    # 1. Encontrar e ler arquivos PGN de entrada
    try:
        pgn_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pgn")]
        if not pgn_files:
            print(f"Nenhum arquivo .pgn encontrado em {INPUT_DIR}")
            print("Por favor, adicione seus 3 PGNs de amostra lá.")
            return
    except FileNotFoundError:
        print(f"Erro: Diretório de entrada não encontrado: {INPUT_DIR}")
        print("Por favor, crie o diretório e adicione seus PGNs.")
        return

    print(f"Encontrados {len(pgn_files)} PGNs para processar.")

    # 2. Processar cada arquivo usando o ext_parser
    for pgn_filename in pgn_files:
        filepath = os.path.join(INPUT_DIR, pgn_filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                pgn_content = f.read()
                
            game_moves = list(parse_annotated_pgn(pgn_content))
            all_moves_data.extend(game_moves)
            
        except Exception as e:
            print(f"Erro ao processar o arquivo {pgn_filename}: {e}")
            import traceback
            traceback.print_exc()

    if not all_moves_data:
        print("Nenhum dado de lance foi extraído.")
        return

    # 3. Salvar dados consolidados em um CSV
    print(f"Processamento concluído. {len(all_moves_data)} lances analisados.")
    
    df = pd.DataFrame(all_moves_data)
    
    # Reordenar colunas para melhor legibilidade
    # Colunas principais (análise de lance) primeiro
    move_cols = [
        "GameId", "ply", "move_number", "player", "move_san", 
        "classification", "centipawn_loss", "eval_cp_pov_white", 
        "eval_change_str", "suggested_best_move", "time_on_clock",
        "fen_before_move", "raw_annotation"
    ]
    
    # Metadados do Jogo (headers) depois
    game_cols = [
        "Event", "Site", "Date", "White", "Black", "Result", 
        "WhiteElo", "BlackElo", "Opening", "ECO", "TimeControl", 
        "Variant", "Termination", "Annotator"
    ]
    
    # Garante que todas as colunas existam, mesmo que o PGN não as tenha
    final_columns = []
    for col in move_cols + game_cols:
        if col in df.columns:
            final_columns.append(col)
            
    df = df[final_columns]
    
    try:
        df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8')
        print(f"Pipeline concluído. Dados salvos em: {OUTPUT_FILENAME}")
    except IOError as e:
        print(f"Erro ao salvar arquivo CSV: {e}")

if __name__ == "__main__":
    # Para executar este pipeline de forma independente:
    # 1. Salve os 3 PGNs que você enviou na pasta 'data/annotated_pgns/'
    # 2. Execute: python ext_pipeline.py
    run_annotated_pipeline()
