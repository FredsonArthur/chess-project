"""Programa principal para testar a movimentação do Bispo"""

from src.core.board import Board
from src.core.constants import Color, PieceType

def mostrar_tabuleiro(board):
    """Exibe o tabuleiro com informações adicionais"""
    print("\n" + "=" * 50)
    print("♝ TESTE DO BISPO")
    print("=" * 50)
    print(board)
    print("\n" + "-" * 50)
    
    # Mostra posição do bispo
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.type == PieceType.BISHOP:
                print(f"📍 Bispo {'BRANCO' if piece.color == Color.WHITE else 'PRETO'} em: {chr(97+col)}{8-row}")
                moves = piece.get_possible_moves(board, (row, col))
                print(f"🎯 Movimentos possíveis: {len(moves)}")
                
                # Organiza movimentos por direção
                print("\n📋 MOVIMENTOS POR DIREÇÃO:")
                moves_por_direcao = {
                    "Cima-Esquerda": [],
                    "Cima-Direita": [],
                    "Baixo-Esquerda": [],
                    "Baixo-Direita": []
                }
                
                for r, c in moves:
                    if r < row and c < col:
                        moves_por_direcao["Cima-Esquerda"].append(f"{chr(97+c)}{8-r}")
                    elif r < row and c > col:
                        moves_por_direcao["Cima-Direita"].append(f"{chr(97+c)}{8-r}")
                    elif r > row and c < col:
                        moves_por_direcao["Baixo-Esquerda"].append(f"{chr(97+c)}{8-r}")
                    elif r > row and c > col:
                        moves_por_direcao["Baixo-Direita"].append(f"{chr(97+c)}{8-r}")
                
                for direcao, posicoes in moves_por_direcao.items():
                    if posicoes:
                        print(f"  ↗ {direcao}: {', '.join(posicoes)}")
                
                break
    print("-" * 50)

def testar_bispo():
    """Testa os movimentos do Bispo"""
    board = Board()
    
    print("\n🎮 TESTE DE MOVIMENTAÇÃO DO BISPO")
    print("=" * 50)
    print("\n📌 LEGENDA:")
    print("  ♗ = Bispo (sua peça)")
    print("  ♙ = Peão aliado (bloqueia)")
    print("  ♟ = Peão inimigo (pode capturar)")
    print("  ♜ = Torre inimiga (bloqueada atrás de peão)")
    print("  · = Casa vazia (pode mover)")
    print("=" * 50)
    
    mostrar_tabuleiro(board)
    
    # Encontra o bispo
    bispo_pos = None
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.type == PieceType.BISHOP:
                bispo_pos = (row, col)
                break
        if bispo_pos:
            break
    
    if not bispo_pos:
        print("❌ Bispo não encontrado no tabuleiro!")
        return
    
    print("\n📋 ANÁLISE DOS MOVIMENTOS:")
    print("-" * 30)
    
    # Lista de movimentos para testar
    testes = [
        # Diagonal Cima-Esquerda
        (3, 3, "e5", "Cima-Esquerda - peão inimigo (CAPTURA)"),
        (2, 2, "f6", "Cima-Esquerda - peão aliado (BLOQUEADO)"),
        (1, 1, "g7", "Cima-Esquerda - além do aliado (BLOQUEADO)"),
        
        # Diagonal Cima-Direita
        (3, 5, "e3", "Cima-Direita - casa vazia (VÁLIDO)"),
        (2, 6, "f2", "Cima-Direita - peão aliado (BLOQUEADO)"),
        (1, 7, "g1", "Cima-Direita - além do aliado (BLOQUEADO)"),
        
        # Diagonal Baixo-Esquerda
        (5, 3, "c5", "Baixo-Esquerda - casa vazia (VÁLIDO)"),
        (6, 2, "b6", "Baixo-Esquerda - peão aliado (BLOQUEADO)"),
        (7, 1, "a7", "Baixo-Esquerda - além do aliado (BLOQUEADO)"),
        
        # Diagonal Baixo-Direita
        (5, 5, "c3", "Baixo-Direita - peão inimigo (CAPTURA)"),
        (6, 6, "b2", "Baixo-Direita - peão inimigo (CAPTURA)"),
        (7, 7, "a1", "Baixo-Direita - além do inimigo (BLOQUEADO)"),
    ]
    
    for row, col, pos, desc in testes:
        moves = board.get_piece(*bispo_pos).get_possible_moves(board, bispo_pos)
        if (row, col) in moves:
            print(f"✅ {pos} → VÁLIDO - {desc}")
        else:
            print(f"❌ {pos} → INVÁLIDO - {desc}")
    
    print("\n" + "=" * 50)
    
    # Loop interativo
    print("\n🎮 MODO INTERATIVO")
    print("Digite um movimento no formato 'd4 e5' para mover o bispo")
    print("Digite 'sair' para encerrar")
    print("Digite 'ajuda' para ver os movimentos válidos")
    print("-" * 50)
    
    while True:
        try:
            cmd = input("\n🔹 Digite um movimento: ").strip().lower()
            
            if cmd == 'sair':
                print("\n👋 Saindo...")
                break
            elif cmd == 'ajuda':
                piece = board.get_piece(*bispo_pos)
                moves = piece.get_possible_moves(board, bispo_pos)
                print(f"\n📍 Movimentos válidos de {chr(97+bispo_pos[1])}{8-bispo_pos[0]}:")
                moves_str = [f"{chr(97+c)}{8-r}" for r, c in moves]
                print(f"   {', '.join(sorted(moves_str))}")
                continue
            
            if ' ' in cmd:
                from_pos, to_pos = cmd.split()
                
                if len(from_pos) != 2 or len(to_pos) != 2:
                    print("❌ Formato inválido! Use 'e4 e5'")
                    continue
                
                from_col = ord(from_pos[0]) - 97
                from_row = 8 - int(from_pos[1])
                to_col = ord(to_pos[0]) - 97
                to_row = 8 - int(to_pos[1])
                
                if not (0 <= from_row < 8 and 0 <= from_col < 8 and 
                        0 <= to_row < 8 and 0 <= to_col < 8):
                    print("❌ Coordenadas fora do tabuleiro! Use a-h e 1-8")
                    continue
                
                if board.move_piece((from_row, from_col), (to_row, to_col)):
                    print("✅ Movimento realizado com sucesso!")
                    bispo_pos = (to_row, to_col)
                    mostrar_tabuleiro(board)
                else:
                    print("❌ Movimento inválido!")
            else:
                print("❌ Use o formato: 'd4 e5'")
                
        except (ValueError, IndexError):
            print("❌ Coordenadas inválidas!")
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break

if __name__ == "__main__":
    testar_bispo()