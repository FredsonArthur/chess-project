"""Classe base para peças de xadrez"""

from typing import List, Tuple, Optional
from .constants import Color, PieceType, PIECE_SYMBOLS

class Piece:
    """Classe base para todas as peças"""
    
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.type = piece_type
        self.has_moved = False
        self._symbol = PIECE_SYMBOLS.get((color, piece_type), '?')
    
    def __str__(self) -> str:
        return self._symbol
    
    def __repr__(self) -> str:
        return f"Piece({self.color.value}, {self.type.value})"
    
    def get_possible_moves(self, board, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Retorna todos os movimentos possíveis para esta peça"""
        row, col = position
        
        if self.type == PieceType.ROOK:
            return self._get_rook_moves(board, row, col)
        elif self.type == PieceType.BISHOP:  # ADICIONADO
            return self._get_bishop_moves(board, row, col)
        
        return []
    
    def _get_rook_moves(self, board, row: int, col: int) -> List[Tuple[int, int]]:
        """Movimentos da Torre - linhas retas (horizontal e vertical)"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_valid_position(r, c):
                if board.is_empty(r, c):
                    moves.append((r, c))
                elif board.is_enemy(r, c, self.color):
                    moves.append((r, c))
                    break
                else:  # Aliada
                    break
                r += dr
                c += dc
        
        return moves
    
    def _get_bishop_moves(self, board, row: int, col: int) -> List[Tuple[int, int]]:
        """
        MOVIMENTOS DO BISPO:
        - Move em diagonais (4 direções)
        - Pode mover quantas casas quiser
        - Não pode pular outras peças
        - Captura a primeira peça inimiga no caminho
        - Não pode mover para casa ocupada por peça aliada
        - Nunca muda de cor (permanece nas diagonais)
        """
        moves = []
        
        # Direções diagonais: cima-esquerda, cima-direita, baixo-esquerda, baixo-direita
        directions = [
            (-1, -1),  # Cima-esquerda
            (-1, 1),   # Cima-direita
            (1, -1),   # Baixo-esquerda
            (1, 1)     # Baixo-direita
        ]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            
            # Continua na direção enquanto estiver dentro do tabuleiro
            while board.is_valid_position(r, c):
                # Se a casa está vazia, pode mover
                if board.is_empty(r, c):
                    moves.append((r, c))
                # Se tem uma peça inimiga, pode capturar (mas para por aqui)
                elif board.is_enemy(r, c, self.color):
                    moves.append((r, c))
                    break  # Para após capturar
                # Se tem uma peça aliada, não pode passar
                else:  # board.is_ally(r, c, self.color)
                    break  # Para antes da peça aliada
                
                # Avança para a próxima casa na mesma direção
                r += dr
                c += dc
        
        return moves