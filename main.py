"""Programa principal para testar a movimentação da Torre"""

from src.core.board import Board
from src.core.piece import Piece
from src.core.constants import Color, PieceType

def mostrar_tabuleiro(board):
    """Exibe o tabuleiro com informações adicionais"""
    print("\n" + "=" * 50)
    print("🏰 TESTE DA TORRE")
    print("=" * 50)
    print(board)
    print("\n" + "-" * 50)
    
    # Mostra posição da torre
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.type == PieceType.ROOK:
                print(f"📍 Torre BRANCA em: {chr(97+col)}{8-row}")
                moves = piece.get_possible_moves(board, (row, col))
                print(f"🎯 Movimentos possíveis: {len(moves)}")
                for r, c in moves:
                    print(f"   → {chr(97+c)}{8-r}")
                break
    print("-" * 50)

def testar_movimentos():
    """Testa os movimentos da Torre"""
    board = Board()
    
    print("\n🎮 TESTE DE MOVIMENTAÇÃO DA TORRE")
    print("=" * 50)
    
    # Mostra o tabuleiro inicial
    mostrar_tabuleiro(board)
    
    # Encontra a torre
    torre_pos = None
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.type == PieceType.ROOK:
                torre_pos = (row, col)
                break
        if torre_pos:
            break
    
    if not torre_pos:
        print("❌ Torre não encontrada no tabuleiro!")
        return
    
    # Testa movimentos
    print("\n📋 TESTANDO MOVIMENTOS:")
    print("-" * 30)
    
    # Lista de movimentos para testar
    testes = [
        (4, 7),   # Direita - deve ser bloqueado por peça aliada
        (4, 3),   # Esquerda - deve capturar peça inimiga
        (2, 4),   # Cima - deve ser bloqueado por peça aliada
        (6, 4),   # Baixo - deve capturar peça inimiga
        (7, 4),   # Baixo - deve ser bloqueado pela peça inimiga após captura
        (4, 1),   # Esquerda - deve ser bloqueado por peça aliada
    ]
    
    for row, col in testes:
        pos_str = f"{chr(97+col)}{8-row}"
        if (row, col) in board.get_piece(*torre_pos).get_possible_moves(board, torre_pos):
            print(f"✅ {pos_str} → MOVIMENTO VÁLIDO")
        else:
            print(f"❌ {pos_str} → MOVIMENTO INVÁLIDO")
    
    print("\n" + "=" * 50)
    
    # Pergunta se quer testar um movimento específico
    while True:
        try:
            cmd = input("\n🔹 Digite um movimento (ex: d4 d6) ou 'sair': ").strip().lower()
            if cmd == 'sair':
                break
            
            if ' ' in cmd:
                from_pos, to_pos = cmd.split()
                from_col = ord(from_pos[0]) - 97
                from_row = 8 - int(from_pos[1])
                to_col = ord(to_pos[0]) - 97
                to_row = 8 - int(to_pos[1])
                
                if board.move_piece((from_row, from_col), (to_row, to_col)):
                    print("✅ Movimento realizado com sucesso!")
                    mostrar_tabuleiro(board)
                else:
                    print("❌ Movimento inválido!")
            else:
                print("❌ Use o formato: 'e4 e5'")
                
        except (ValueError, IndexError):
            print("❌ Coordenadas inválidas! Use letras de a-h e números de 1-8")

if __name__ == "__main__":
    testar_movimentos()