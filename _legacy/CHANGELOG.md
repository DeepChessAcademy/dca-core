# Changelog

Todo o histórico de mudanças notáveis neste projeto será documentado neste arquivo.
O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [4.0.0] - 2025-11-14

### Corrigido (Fixed)

* `[Lógica de Rede]` Corrigida a lógica de visualização de redes, que exibia múltiplos itens no menu suspenso que resultavam em um destaque visual idêntico. Isso acontecia porque a visualização recursiva de defesa destacava o mesmo "complexo defensivo" para várias redes táticas diferentes.

### Adicionado (Added)

* `[Lógica de Rede]` Implementada uma "assinatura visual" (`getNetworkVisualSignature`) para cada rede, baseada no conjunto único de casas escuras e claras que seriam destacadas.

### Alterado (Changed)

* `[UI/UX]` O menu suspenso de "Redes de Impacto" (`populateNetworkSelector`) agora usa um `Map` para filtrar redes pela sua "assinatura visual", exibindo apenas **redes visualmente únicas**.
* `[UI/UX]` Renomeado o card de "Redes" para "Redes (Visuais Únicas)" para refletir a nova lógica de filtragem.

## [3.0.0]

### Adicionado (Added)

* `[Segurança do Rei]` Adicionada a detecção de **Ameaças em Diagonais** (`checkOpenDiagonals`). A ferramenta agora identifica Bispos e Damas inimigas em "raio-x" contra o Rei (quando não há peões amigos bloqueando o caminho).
* `[Segurança do Rei]` A lógica de colunas (`checkOpenFiles`) agora diferencia entre colunas "Abertas" (sem peões) e "**Semi-Abertas**" (sem peões *amigos*), que são as mais perigosas para o Rei.

### Alterado (Changed)

* `[UI/UX]` Renomeado o termo "Arquivos Próximos" para "**Colunas Próximas**" no card de "Segurança do Rei" para usar a terminologia correta de xadrez em português.

## [2.0.0]

### Adicionado (Added)

* `[Avaliação]` Implementado um motor de **Avaliação Estática** completo, que serve de base para todos os novos cartões de pontuação.
* `[Avaliação]` Adicionado **Balanço Material Ponderado** (Dama=9, Torre=5, Bispo=3, Cavalo=3, Peão=1).
* `[Avaliação]` Adicionada **Pontuação Posicional (PST)**, usando *centipawns* e *Piece-Square Tables* (PSTs) para avaliar a qualidade da casa de cada peça.
* `[Avaliação]` Adicionada **Análise de Estrutura de Peões**, que detecta peões Dobrados, Isolados e Passados para ambas as cores.
* `[Avaliação]` Adicionada detecção de **Vulnerabilidades Táticas** (Peças Suspensas e Peças Sobrecarregadas).
* `[UI/UX]` Adicionado um **Sumário de Pontuação Total** no topo do painel, que combina (Material + Posição).
* `[UI/UX]` Adicionado o card "Visão Geral de Peças" com status tático/mobilidade (ex: 🔴 SUSPENSA, 🟠 SOBRECARREGADA, BLOQUEADA).
* `[UI/UX]` Adicionados novos cards de análise para Material, Posição, Estrutura de Peões e Segurança do Rei.

## [1.0.0]

### Adicionado (Added)

* Criação inicial do projeto.
* Renderização do tabuleiro de xadrez a partir de uma string FEN.
* Painel de análise interativo.
* Análise de **Pontos de Contato** (Ataque/Defesa).
* Análise de **Mobilidade** (Peças Bloqueadas/Limitadas).
* Análise de **Redes de Composição** (cadeias de 2 passos: A 🡒 B 🡒 C).
* Visualizador de redes de impacto no tabuleiro com destaque hierárquico (escuro/claro).
* Handler de clique para análise detalhada por casa e por peça.

