"""Testes unitários para as peças de xadrez"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.board import Board
from src.core.piece import Piece
from src.core.constants import Color, PieceType

# ==================== TESTES DA TORRE ====================

class TestRook(unittest.TestCase):
    """Testa a movimentação da Torre"""
    
    def setUp(self):
        self.board = Board()
        for row in range(8):
            for col in range(8):
                self.board.grid[row][col] = None
    
    def test_rook_moves_empty_board(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertEqual(len(moves), 14)
    
    def test_rook_blocked_by_ally(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        self.board.grid[2][4] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[6][4] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[4][2] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[4][6] = Piece(Color.WHITE, PieceType.PAWN)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertEqual(len(moves), 4)
    
    def test_rook_captures_enemy(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        self.board.grid[0][4] = Piece(Color.BLACK, PieceType.PAWN)
        self.board.grid[7][4] = Piece(Color.BLACK, PieceType.PAWN)
        self.board.grid[4][0] = Piece(Color.BLACK, PieceType.PAWN)
        self.board.grid[4][7] = Piece(Color.BLACK, PieceType.PAWN)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertEqual(len(moves), 14)
    
    def test_rook_cannot_move_diagonally(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        diagonal_moves = [(3,3), (3,5), (5,3), (5,5)]
        for move in diagonal_moves:
            self.assertNotIn(move, moves)
    
    def test_rook_corner_moves(self):
        self.board.grid[7][0] = Piece(Color.WHITE, PieceType.ROOK)
        moves = self.board.get_piece(7, 0).get_possible_moves(self.board, (7, 0))
        self.assertEqual(len(moves), 14)
    
    def test_rook_blocked_after_capture(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        self.board.grid[6][4] = Piece(Color.BLACK, PieceType.PAWN)
        self.board.grid[7][4] = Piece(Color.BLACK, PieceType.ROOK)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertIn((6, 4), moves)
        self.assertNotIn((7, 4), moves)
    
    def test_rook_surrounded_by_allies(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            self.board.grid[4+dr][4+dc] = Piece(Color.WHITE, PieceType.PAWN)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertEqual(len(moves), 0)
    
    def test_rook_black_piece_moves(self):
        self.board.grid[4][4] = Piece(Color.BLACK, PieceType.ROOK)
        self.board.grid[2][4] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[4][6] = Piece(Color.BLACK, PieceType.PAWN)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertIn((3, 4), moves)
        self.assertIn((2, 4), moves)
        self.assertIn((4, 5), moves)
        self.assertNotIn((4, 6), moves)
    
    def test_rook_fully_surrounded_by_enemies(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            self.board.grid[4+dr][4+dc] = Piece(Color.BLACK, PieceType.PAWN)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertEqual(len(moves), 4)
    
    def test_rook_middle_board_complex(self):
        self.board.grid[3][4] = Piece(Color.WHITE, PieceType.ROOK)
        self.board.grid[1][4] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[5][4] = Piece(Color.BLACK, PieceType.PAWN)
        self.board.grid[3][6] = Piece(Color.BLACK, PieceType.PAWN)
        self.board.grid[3][2] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[7][4] = Piece(Color.BLACK, PieceType.ROOK)
        moves = self.board.get_piece(3, 4).get_possible_moves(self.board, (3, 4))
        self.assertEqual(len(moves), 6)
    
    def test_rook_movement_after_move(self):
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        self.board.move_piece((4, 4), (3, 4))
        self.assertIsNone(self.board.get_piece(4, 4))
        self.assertIsNotNone(self.board.get_piece(3, 4))
        moves = self.board.get_piece(3, 4).get_possible_moves(self.board, (3, 4))
        self.assertGreater(len(moves), 0)


# ==================== TESTES DO BISPO ====================

class TestBishop(unittest.TestCase):
    """Testa a movimentação do Bispo"""
    
    def setUp(self):
        """Configura um tabuleiro limpo para cada teste"""
        self.board = Board()
        for row in range(8):
            for col in range(8):
                self.board.grid[row][col] = None
    
    def test_bishop_moves_empty_board(self):
        """Testa movimentos do Bispo em um tabuleiro vazio"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Em d4: 4+3+3+3 = 13 movimentos
        self.assertEqual(len(moves), 13, f"Esperado 13, mas tem {len(moves)}")
        
        expected_moves = [
            (3, 3), (2, 2), (1, 1), (0, 0),  # Cima-Esquerda
            (3, 5), (2, 6), (1, 7),           # Cima-Direita
            (5, 3), (6, 2), (7, 1),           # Baixo-Esquerda
            (5, 5), (6, 6), (7, 7),           # Baixo-Direita
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Movimento {move} não encontrado")
    
    def test_bishop_blocked_by_ally(self):
        """Testa se o Bispo é bloqueado por peças aliadas"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        
        self.board.grid[2][2] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[2][6] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[6][2] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[6][6] = Piece(Color.WHITE, PieceType.PAWN)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        expected_moves = [(3, 3), (3, 5), (5, 3), (5, 5)]
        not_expected = [(2, 2), (2, 6), (6, 2), (6, 6)]
        
        for move in expected_moves:
            self.assertIn(move, moves)
        for move in not_expected:
            self.assertNotIn(move, moves)
        
        self.assertEqual(len(moves), 4)
    
    def test_bishop_captures_enemy(self):
        """Testa se o Bispo pode capturar peças inimigas"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        
        # Peças inimigas nas diagonais
        self.board.grid[0][0] = Piece(Color.BLACK, PieceType.PAWN)  # a8
        self.board.grid[1][7] = Piece(Color.BLACK, PieceType.PAWN)  # h7
        self.board.grid[7][1] = Piece(Color.BLACK, PieceType.PAWN)  # a7 (CORRIGIDO)
        self.board.grid[7][7] = Piece(Color.BLACK, PieceType.PAWN)  # h1
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        expected_moves = [
            (3, 3), (2, 2), (1, 1), (0, 0),
            (3, 5), (2, 6), (1, 7),
            (5, 3), (6, 2), (7, 1),  # CORRIGIDO: (7,1) em vez de (7,0)
            (5, 5), (6, 6), (7, 7),
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Movimento {move} deveria estar disponível")
        
        self.assertEqual(len(moves), 13)
    
    def test_bishop_blocked_after_capture(self):
        """Testa se o Bispo para após capturar uma peça"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        
        self.board.grid[3][5] = Piece(Color.BLACK, PieceType.PAWN)  # e5
        self.board.grid[2][6] = Piece(Color.BLACK, PieceType.ROOK)  # f6
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        self.assertIn((3, 5), moves, "Deveria capturar o peão em e5")
        self.assertNotIn((2, 6), moves, "Não deveria capturar a torre em f6")
        self.assertIn((3, 3), moves)
        self.assertIn((5, 3), moves)
        self.assertIn((5, 5), moves)
    
    def test_bishop_corner_moves(self):
        """Testa movimentos do Bispo nos cantos"""
        self.board.grid[7][0] = Piece(Color.WHITE, PieceType.BISHOP)
        moves = self.board.get_piece(7, 0).get_possible_moves(self.board, (7, 0))
        
        self.assertEqual(len(moves), 7)
        
        expected_moves = [
            (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves)
    
    def test_bishop_middle_board_complex(self):
        """Testa movimentos do Bispo com várias peças"""
        self.board.grid[3][4] = Piece(Color.WHITE, PieceType.BISHOP)  # e5
        
        self.board.grid[1][2] = Piece(Color.WHITE, PieceType.PAWN)  # c7 (aliada)
        self.board.grid[5][2] = Piece(Color.BLACK, PieceType.PAWN)  # c3 (inimiga)
        self.board.grid[5][6] = Piece(Color.BLACK, PieceType.PAWN)  # g3 (inimiga)
        self.board.grid[1][6] = Piece(Color.WHITE, PieceType.PAWN)  # g7 (aliada)
        self.board.grid[7][0] = Piece(Color.BLACK, PieceType.ROOK)  # a1
        
        moves = self.board.get_piece(3, 4).get_possible_moves(self.board, (3, 4))
        
        self.assertIn((2, 3), moves)
        self.assertNotIn((1, 2), moves)
        self.assertIn((4, 3), moves)
        self.assertIn((5, 2), moves)
        self.assertNotIn((6, 1), moves)
        self.assertNotIn((7, 0), moves)
        self.assertIn((2, 5), moves)
        self.assertNotIn((1, 6), moves)
        self.assertIn((4, 5), moves)
        self.assertIn((5, 6), moves)
    
    def test_bishop_cannot_move_orthogonally(self):
        """Testa se o Bispo NÃO pode se mover ortogonalmente"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        orthogonal_moves = [(3, 4), (5, 4), (4, 3), (4, 5), (2, 4), (6, 4), (4, 2), (4, 6)]
        
        for move in orthogonal_moves:
            self.assertNotIn(move, moves)
    
    def test_bishop_black_piece_moves(self):
        """Testa movimentos de um Bispo preto"""
        self.board.grid[4][4] = Piece(Color.BLACK, PieceType.BISHOP)
        self.board.grid[2][2] = Piece(Color.WHITE, PieceType.PAWN)
        self.board.grid[6][6] = Piece(Color.BLACK, PieceType.PAWN)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        self.assertIn((3, 3), moves)
        self.assertIn((2, 2), moves)
        self.assertIn((5, 5), moves)
        self.assertNotIn((6, 6), moves)
    
    def test_bishop_surrounded_by_allies(self):
        """Testa Bispo cercado por aliados (sem movimentos)"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            self.board.grid[4+dr][4+dc] = Piece(Color.WHITE, PieceType.PAWN)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        self.assertEqual(len(moves), 0)
    
    def test_bishop_fully_surrounded_by_enemies(self):
        """Testa Bispo cercado por inimigos (só captura as 4 diagonais)"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            self.board.grid[4+dr][4+dc] = Piece(Color.BLACK, PieceType.PAWN)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        self.assertEqual(len(moves), 4)
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            self.assertIn((4+dr, 4+dc), moves)
    
    def test_bishop_same_color_squares(self):
        """Testa se o Bispo permanece nas casas da mesma cor"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.BISHOP)
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # d4 é casa escura (soma par)
        for row, col in moves:
            soma = row + col
            self.assertEqual(soma % 2, 0, 
                           f"Bispo moveu para casa de cor diferente: {chr(97+col)}{8-row}")

if __name__ == '__main__':
    unittest.main(verbosity=2)