"""Classe base para peças de xadrez - Implementação inicial apenas com Torre"""

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
        
        # POR ENQUANTO: APENAS TORRE
        if self.type == PieceType.ROOK:
            return self._get_rook_moves(board, row, col)
        
        # Outras peças serão implementadas depois
        return []
    
    def _get_rook_moves(self, board, row: int, col: int) -> List[Tuple[int, int]]:
        """
        MOVIMENTOS DA TORRE:
        - Move em linhas retas (horizontais e verticais)
        - Pode mover quantas casas quiser
        - Não pode pular outras peças
        - Captura a primeira peça inimiga no caminho
        - Não pode mover para casa ocupada por peça aliada
        """
        moves = []
        
        # Direções: cima, baixo, esquerda, direita
        directions = [
            (-1, 0),  # Cima (diminui linha)
            (1, 0),   # Baixo (aumenta linha)
            (0, -1),  # Esquerda (diminui coluna)
            (0, 1)    # Direita (aumenta coluna)
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