"""Constantes do jogo de xadrez"""

from enum import Enum

class Color(Enum):
    """Cores das peças"""
    WHITE = "white"
    BLACK = "black"
    
    def opposite(self):
        """Retorna a cor oposta"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE

class PieceType(Enum):
    """Tipos de peças"""
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

# Símbolos Unicode para peças
PIECE_SYMBOLS = {
    (Color.WHITE, PieceType.ROOK): '♖',
    (Color.BLACK, PieceType.ROOK): '♜',
    (Color.WHITE, PieceType.BISHOP): '♗',  # ADICIONADO
    (Color.BLACK, PieceType.BISHOP): '♝',  # ADICIONADO
    (Color.WHITE, PieceType.PAWN): '♙',
    (Color.BLACK, PieceType.PAWN): '♟',
}