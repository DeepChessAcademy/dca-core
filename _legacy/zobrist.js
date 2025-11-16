// zobrist.js

/**
 * Módulo de Hashing Zobrist para Posições de Xadrez (Vanilla JS)
 *
 * Este módulo gera hashes Zobrist de 64 bits (BigInt) a partir de FEN strings.
 * É crucial para detecção de transposições em engines de xadrez.
 *
 * Baseado no conceito de:
 * 1. Chaves aleatórias de 64 bits para cada [peça][cor][casa].
 * 2. Chaves para o lado a mover, direitos de roque e casa de en passant.
 * 3. O hash final é um XOR de todas as chaves relevantes.
 */

// --- Constantes (para indexação) ---
const PIECES = { P: 0, N: 1, B: 2, R: 3, Q: 4, K: 5 };
const COLORS = { W: 0, B: 1 };
const SQUARES = 64;

// --- Tabelas Zobrist (preenchidas por initZobristKeys) ---

// Tabela 3D: [tipo_peça][cor][casa]
// Usamos '0n' para indicar que são BigInts.
let zobristTable = Array(6).fill(null).map(() => 
    Array(2).fill(null).map(() => 
        Array(SQUARES).fill(0n)
    )
);

// Chave para "Pretas a mover" (XORado se for a vez das pretas)
let zobristSideToMove = 0n;

// Chaves para direitos de roque [16 combinações de K, Q, k, q]
let zobristCastling = Array(16).fill(0n);

// Chaves para a COLUNA de en passant [8 colunas + 1 para "nenhum"]
let zobristEnPassant = Array(9).fill(0n); // 0-7 para colunas a-h, 8 para '-'

/**
 * Gera um número aleatório seguro de 64 bits como BigInt.
 * Usa a API Crypto do browser/Node.js, que é a "melhor prática" em Vanilla JS.
 * @returns {BigInt}
 */
function _generateRandom64Bit() {
    const arr = new BigUint64Array(1);
    // `crypto.getRandomValues` é o padrão web moderno para aleatoriedade.
    crypto.getRandomValues(arr);
    return arr[0];
}

/**
 * (API) Inicializa todas as tabelas Zobrist com chaves aleatórias de 64 bits.
 * DEVE ser chamada uma (e apenas uma) vez antes de gerar qualquer hash.
 */
export function initZobristKeys() {
    // 1. Preenche a tabela de Peça/Cor/Casa
    for (let p = 0; p < 6; p++) { // P, N, B, R, Q, K
        for (let c = 0; c < 2; c++) { // White, Black
            for (let s = 0; s < SQUARES; s++) { // 0-63
                zobristTable[p][c][s] = _generateRandom64Bit();
            }
        }
    }

    // 2. Chave de Lado a Mover
    zobristSideToMove = _generateRandom64Bit();

    // 3. Chaves de Roque (16 possibilidades)
    for (let i = 0; i < 16; i++) {
        zobristCastling[i] = _generateRandom64Bit();
    }

    // 4. Chaves de En Passant (8 colunas + 1 para "nenhum")
    for (let i = 0; i < 9; i++) {
        zobristEnPassant[i] = _generateRandom64Bit();
    }
}

/**
 * (API) Gera um hash Zobrist para um FEN string completo.
 * @param {string} fen - O FEN string (ex: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
 * @returns {BigInt} O hash Zobrist de 64 bits.
 */
export function generateZobristHash(fen) {
    const parts = fen.split(' ');
    if (parts.length < 4) {
        throw new Error("FEN inválido. Deve ter pelo menos 4 partes.");
    }

    const boardStr = parts[0];
    const side = parts[1];
    const castling = parts[2];
    const enPassant = parts[3];

    // O '0n' inicializa o acumulador como um BigInt.
    let hash = 0n;

    // --- 1. Posição das Peças ---
    let rank = 7; // FEN começa em a8 (rank 7)
    let file = 0; // file 0
    for (const char of boardStr) {
        if (char === '/') {
            rank--;
            file = 0;
        } else if (/\d/.test(char)) {
            // Avança o número de casas vazias
            file += parseInt(char, 10);
        } else {
            // É uma peça
            const color = (char === char.toUpperCase()) ? COLORS.W : COLORS.B;
            const piece = PIECES[char.toUpperCase()];
            const square = rank * 8 + file;
            
            // O coração do Zobrist: XORa a chave da peça
            hash ^= zobristTable[piece][color][square];
            file++;
        }
    }

    // --- 2. Lado a Mover ---
    if (side === 'b') {
        hash ^= zobristSideToMove;
    }

    // --- 3. Direitos de Roque ---
    // Criamos um índice de 4 bits: K Q k q (ex: 1101 = 13)
    let castlingRights = 0;
    if (castling.includes('K')) castlingRights |= 1;
    if (castling.includes('Q')) castlingRights |= 2;
    if (castling.includes('k')) castlingRights |= 4;
    if (castling.includes('q')) castlingRights |= 8;
    
    hash ^= zobristCastling[castlingRights];

    // --- 4. En Passant ---
    if (enPassant !== '-') {
        const file = enPassant.charCodeAt(0) - 'a'.charCodeAt(0); // 'a' -> 0, 'h' -> 7
        hash ^= zobristEnPassant[file];
    } else {
        hash ^= zobristEnPassant[8]; // Chave para "nenhum en passant"
    }

    return hash;
}
