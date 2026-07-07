"""Classe do tabuleiro de xadrez - Versão simplificada para testar a Torre"""

from typing import Optional, List, Tuple
from .constants import Color, PieceType
from .piece import Piece

class Board:
    """Representa o tabuleiro de xadrez 8x8"""
    
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_test_board()  # Configura um tabuleiro de teste
    
    def _setup_test_board(self):
        """Configura um tabuleiro de teste com apenas algumas peças"""
        # Limpa o tabuleiro
        for row in range(8):
            for col in range(8):
                self.grid[row][col] = None
        
        # Coloca uma TORRE BRANCA no centro (posição 4,4)
        self.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Coloca algumas peças para testar movimentos
        # Peças aliadas (bloqueiam o caminho)
        self.grid[4][6] = Piece(Color.WHITE, PieceType.PAWN)  # Aliada à direita
        self.grid[2][4] = Piece(Color.WHITE, PieceType.PAWN)  # Aliada acima
        
        # Peças inimigas (podem ser capturadas)
        self.grid[6][4] = Piece(Color.BLACK, PieceType.PAWN)  # Inimiga abaixo
        self.grid[4][2] = Piece(Color.BLACK, PieceType.PAWN)  # Inimiga à esquerda
        
        # Peças para testar bloqueio
        self.grid[7][4] = Piece(Color.BLACK, PieceType.ROOK)  # Inimiga mais abaixo
        self.grid[4][0] = Piece(Color.WHITE, PieceType.PAWN)  # Aliada mais à esquerda
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Verifica se a posição está dentro do tabuleiro"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_empty(self, row: int, col: int) -> bool:
        """Verifica se a posição está vazia"""
        if not self.is_valid_position(row, col):
            return False
        return self.grid[row][col] is None
    
    def is_ally(self, row: int, col: int, color: Color) -> bool:
        """Verifica se a posição contém uma peça aliada"""
        if not self.is_valid_position(row, col):
            return False
        piece = self.grid[row][col]
        return piece is not None and piece.color == color
    
    def is_enemy(self, row: int, col: int, color: Color) -> bool:
        """Verifica se a posição contém uma peça inimiga"""
        if not self.is_valid_position(row, col):
            return False
        piece = self.grid[row][col]
        return piece is not None and piece.color != color
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Retorna a peça em uma posição"""
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return None
    
    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Move uma peça de uma posição para outra (SIMPLIFICADO)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return False
        
        # Verifica se o movimento é válido
        possible_moves = piece.get_possible_moves(self, from_pos)
        if to_pos not in possible_moves:
            return False
        
        # Realiza o movimento
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        piece.has_moved = True
        
        return True
    
    def __str__(self) -> str:
        """Representação em ASCII do tabuleiro"""
        result = "  a b c d e f g h\n"
        for row in range(8):
            result += f"{8 - row} "
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    result += str(piece) + " "
                else:
                    result += "· "
            result += f"{8 - row}\n"
        result += "  a b c d e f g h"
        return result