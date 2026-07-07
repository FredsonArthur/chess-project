"""Classe do tabuleiro de xadrez"""

from typing import Optional, List, Tuple
from .constants import Color, PieceType
from .piece import Piece

class Board:
    """Representa o tabuleiro de xadrez 8x8"""
    
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_test_board()
    
    def _setup_test_board(self):
        """Configura um tabuleiro de teste com Torre e Bispo"""
        # Limpa o tabuleiro
        for row in range(8):
            for col in range(8):
                self.grid[row][col] = None
        
        # ===== BISPO BRANCO no centro (d4) =====
        self.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        
        # ===== PEÇAS PARA TESTAR O BISPO =====
        
        # Peças aliadas (bloqueiam o caminho)
        self.grid[2][2] = Piece(Color.WHITE, PieceType.PAWN)  # f6 (diagonal cima-esquerda)
        self.grid[2][6] = Piece(Color.WHITE, PieceType.PAWN)  # b6 (diagonal cima-direita)
        self.grid[6][2] = Piece(Color.WHITE, PieceType.PAWN)  # f2 (diagonal baixo-esquerda)
        
        # Peças inimigas (podem ser capturadas)
        self.grid[6][6] = Piece(Color.BLACK, PieceType.PAWN)  # b2 (diagonal baixo-direita)
        self.grid[3][3] = Piece(Color.BLACK, PieceType.PAWN)  # e5 (diagonal cima-esquerda)
        self.grid[5][5] = Piece(Color.BLACK, PieceType.PAWN)  # c3 (diagonal baixo-direita)
        
        # Peça inimiga mais longe para testar bloqueio após captura
        self.grid[1][1] = Piece(Color.BLACK, PieceType.ROOK)  # g7 (atrás do peão em f6)
        self.grid[7][7] = Piece(Color.BLACK, PieceType.ROOK)  # a1 (atrás do peão em b2)
        
        # ===== TORRE para comparação (opcional) =====
        # self.grid[7][0] = Piece(Color.WHITE, PieceType.ROOK)  # a1
    
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
        """Move uma peça de uma posição para outra"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return False
        
        possible_moves = piece.get_possible_moves(self, from_pos)
        if to_pos not in possible_moves:
            return False
        
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