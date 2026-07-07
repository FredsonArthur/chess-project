"""Testes unitários para as peças de xadrez - Focado na Torre"""

import unittest
import sys
import os

# Adiciona o diretório src ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.board import Board
from src.core.piece import Piece
from src.core.constants import Color, PieceType

class TestRook(unittest.TestCase):
    """Testa todos os aspectos da movimentação da Torre"""
    
    def setUp(self):
        """Configura um tabuleiro limpo para cada teste"""
        self.board = Board()
        # Limpa o tabuleiro
        for row in range(8):
            for col in range(8):
                self.board.grid[row][col] = None
    
    # ==================== TESTES BÁSICOS ====================
    
    def test_rook_moves_empty_board(self):
        """Testa movimentos da Torre em um tabuleiro vazio"""
        # Coloca uma Torre branca no centro (d4)
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Em um tabuleiro vazio, a Torre deve ter 14 movimentos
        # (7 para cima + 7 para baixo + 7 para esquerda + 7 para direita)
        self.assertEqual(len(moves), 14)
        
        # Verifica movimentos específicos
        expected_moves = [
            # Cima (linhas 0-3)
            (3, 4), (2, 4), (1, 4), (0, 4),
            # Baixo (linhas 5-7)
            (5, 4), (6, 4), (7, 4),
            # Esquerda (colunas 0-3)
            (4, 3), (4, 2), (4, 1), (4, 0),
            # Direita (colunas 5-7)
            (4, 5), (4, 6), (4, 7)
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Movimento {move} não encontrado")
    
    def test_rook_corner_moves(self):
        """Testa movimentos da Torre nos cantos do tabuleiro"""
        # Coloca uma Torre branca no canto a1
        self.board.grid[7][0] = Piece(Color.WHITE, PieceType.ROOK)
        
        moves = self.board.get_piece(7, 0).get_possible_moves(self.board, (7, 0))
        
        # Em um tabuleiro vazio, do canto deve ter 14 movimentos
        # (7 para baixo + 7 para direita)
        self.assertEqual(len(moves), 14)
        
        # Verifica movimentos específicos
        expected_moves = [
            # Cima (linhas 0-6)
            (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0),
            # Direita (colunas 1-7)
            (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Movimento {move} não encontrado")
    
    # ==================== TESTES DE BLOQUEIO ====================
    
    def test_rook_blocked_by_ally(self):
        """Testa se a Torre é bloqueada por peças aliadas"""
        # Coloca uma Torre branca em d4
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Coloca peças aliadas bloqueando
        self.board.grid[2][4] = Piece(Color.WHITE, PieceType.PAWN)  # d6 (acima)
        self.board.grid[6][4] = Piece(Color.WHITE, PieceType.PAWN)  # d2 (abaixo)
        self.board.grid[4][2] = Piece(Color.WHITE, PieceType.PAWN)  # b4 (esquerda)
        self.board.grid[4][6] = Piece(Color.WHITE, PieceType.PAWN)  # f4 (direita)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Deve conseguir mover até as peças aliadas, mas não além
        expected_moves = [
            # Cima - até antes da peça aliada em d6 (linha 2)
            (3, 4),
            # Baixo - até antes da peça aliada em d2 (linha 6)
            (5, 4),
            # Esquerda - até antes da peça aliada em b4 (coluna 2)
            (4, 3),
            # Direita - até antes da peça aliada em f4 (coluna 6)
            (4, 5),
        ]
        
        # Não deve incluir as posições das peças aliadas
        not_expected = [(2, 4), (6, 4), (4, 2), (4, 6)]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Movimento {move} deveria estar disponível")
        
        for move in not_expected:
            self.assertNotIn(move, moves, f"Movimento {move} não deveria estar disponível")
        
        # Deve ter exatamente 4 movimentos
        self.assertEqual(len(moves), 4)
    
    def test_rook_surrounded_by_allies(self):
        """Testa Torre cercada por aliados (sem movimentos)"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Cerca completamente a torre com aliados
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            self.board.grid[4+dr][4+dc] = Piece(Color.WHITE, PieceType.PAWN)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Não deve ter nenhum movimento
        self.assertEqual(len(moves), 0)
    
    # ==================== TESTES DE CAPTURA ====================
    
    def test_rook_captures_enemy(self):
        """Testa se a Torre pode capturar peças inimigas"""
        # Coloca uma Torre branca em d4
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Coloca peças inimigas para capturar
        self.board.grid[0][4] = Piece(Color.BLACK, PieceType.PAWN)  # d8 (cima)
        self.board.grid[7][4] = Piece(Color.BLACK, PieceType.PAWN)  # d1 (baixo)
        self.board.grid[4][0] = Piece(Color.BLACK, PieceType.PAWN)  # a4 (esquerda)
        self.board.grid[4][7] = Piece(Color.BLACK, PieceType.PAWN)  # h4 (direita)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Deve poder capturar as peças inimigas
        expected_moves = [
            # Caminho até as peças, incluindo a captura
            (3, 4), (2, 4), (1, 4), (0, 4),  # Captura em d8
            (5, 4), (6, 4), (7, 4),           # Captura em d1
            (4, 3), (4, 2), (4, 1), (4, 0),   # Captura em a4
            (4, 5), (4, 6), (4, 7),           # Captura em h4
        ]
        
        for move in expected_moves:
            self.assertIn(move, moves, f"Movimento {move} deveria estar disponível")
        
        # Deve ter 14 movimentos (todas as direções até o fim)
        self.assertEqual(len(moves), 14)
    
    def test_rook_blocked_after_capture(self):
        """Testa se a Torre para após capturar uma peça"""
        # Coloca uma Torre branca em d4
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Coloca uma peça inimiga em d2 e outra atrás dela em d1
        self.board.grid[6][4] = Piece(Color.BLACK, PieceType.PAWN)  # d2
        self.board.grid[7][4] = Piece(Color.BLACK, PieceType.ROOK)  # d1 (atrás)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Deve capturar o peão em d2, mas não chegar à torre em d1
        self.assertIn((6, 4), moves, "Deveria capturar o peão em d2")
        self.assertNotIn((7, 4), moves, "Não deveria capturar a torre em d1 (bloqueada)")
        
        # Deve conseguir mover para as casas antes do peão
        self.assertIn((5, 4), moves, "Deveria mover para d3")
    
    def test_rook_fully_surrounded_by_enemies(self):
        """Testa Torre completamente cercada por inimigos (só captura)"""
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Cerca completamente a torre com inimigos
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            self.board.grid[4+dr][4+dc] = Piece(Color.BLACK, PieceType.PAWN)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Deve capturar as 4 peças ao redor
        self.assertEqual(len(moves), 4)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            self.assertIn((4+dr, 4+dc), moves)
    
    # ==================== TESTES DE RESTRIÇÕES ====================
    
    def test_rook_cannot_move_diagonally(self):
        """Testa se a Torre NÃO pode se mover na diagonal"""
        # Coloca uma Torre branca em d4
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Movimentos diagonais NÃO devem estar disponíveis
        diagonal_moves = [
            (3, 3), (3, 5),  # Cima-esquerda, Cima-direita
            (5, 3), (5, 5),  # Baixo-esquerda, Baixo-direita
            (2, 2), (2, 6), (6, 2), (6, 6)  # Diagonais mais longas
        ]
        
        for move in diagonal_moves:
            self.assertNotIn(move, moves, f"Movimento diagonal {move} não deveria estar disponível")
    
    # ==================== TESTES DE CORES ====================
    
    def test_rook_black_piece_moves(self):
        """Testa movimentos de uma Torre preta"""
        self.board.grid[4][4] = Piece(Color.BLACK, PieceType.ROOK)
        
        # Coloca peças para testar direções opostas
        self.board.grid[2][4] = Piece(Color.WHITE, PieceType.PAWN)  # Inimiga acima
        self.board.grid[4][6] = Piece(Color.BLACK, PieceType.PAWN)  # Aliada à direita
        
        moves = self.board.get_piece(4, 4).get_possible_moves(self.board, (4, 4))
        
        # Deve capturar a peça inimiga acima
        self.assertIn((3, 4), moves)
        self.assertIn((2, 4), moves)
        
        # Não deve passar pela aliada à direita
        self.assertIn((4, 5), moves)
        self.assertNotIn((4, 6), moves)
    
    # ==================== TESTES DE CENÁRIOS COMPLEXOS ====================
    
    def test_rook_middle_board_complex(self):
        """Testa movimentos da Torre no meio do tabuleiro com várias peças"""
        # Coloca uma Torre branca em e5
        self.board.grid[3][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Configura um cenário complexo
        self.board.grid[1][4] = Piece(Color.WHITE, PieceType.PAWN)  # Aliada em e7
        self.board.grid[5][4] = Piece(Color.BLACK, PieceType.PAWN)  # Inimiga em e3
        self.board.grid[3][6] = Piece(Color.BLACK, PieceType.PAWN)  # Inimiga em g5
        self.board.grid[3][2] = Piece(Color.WHITE, PieceType.PAWN)  # Aliada em c5
        self.board.grid[7][4] = Piece(Color.BLACK, PieceType.ROOK)  # Inimiga em e1
        
        moves = self.board.get_piece(3, 4).get_possible_moves(self.board, (3, 4))
        
        # Verifica movimentos esperados
        # Cima: até antes da aliada em e7 (linha 1)
        self.assertIn((2, 4), moves, "Deveria mover para e6")
        self.assertNotIn((1, 4), moves, "Não deveria capturar aliada em e7")
        
        # Baixo: captura inimiga em e3, mas não chega à torre em e1
        self.assertIn((4, 4), moves, "Deveria mover para e4")
        self.assertIn((5, 4), moves, "Deveria capturar inimiga em e3")
        self.assertNotIn((6, 4), moves, "Não deveria passar da inimiga")
        self.assertNotIn((7, 4), moves, "Não deveria capturar torre em e1")
        
        # Direita: captura inimiga em g5
        self.assertIn((3, 5), moves, "Deveria mover para f5")
        self.assertIn((3, 6), moves, "Deveria capturar inimiga em g5")
        self.assertNotIn((3, 7), moves, "Não deveria passar da inimiga")
        
        # Esquerda: até antes da aliada em c5 (coluna 2)
        self.assertIn((3, 3), moves, "Deveria mover para d5")
        self.assertNotIn((3, 2), moves, "Não deveria capturar aliada em c5")
        
        # Total de movimentos esperados: 
        # Cima: 1 (e6)
        # Baixo: 2 (e4, e3)
        # Direita: 2 (f5, g5)
        # Esquerda: 1 (d5)
        self.assertEqual(len(moves), 6)
    
    def test_rook_movement_after_move(self):
        """Testa se a Torre pode se mover após já ter se movido"""
        # Coloca uma Torre branca em d4
        self.board.grid[4][4] = Piece(Color.WHITE, PieceType.ROOK)
        
        # Movimenta a torre para d5
        self.board.move_piece((4, 4), (3, 4))
        
        # Verifica se a torre está na nova posição
        self.assertIsNone(self.board.get_piece(4, 4), "Torre deveria ter saído de d4")
        self.assertIsNotNone(self.board.get_piece(3, 4), "Torre deveria estar em d5")
        
        # Verifica se a torre pode se mover de d5
        moves = self.board.get_piece(3, 4).get_possible_moves(self.board, (3, 4))
        
        # Deve ter movimentos disponíveis
        self.assertGreater(len(moves), 0, "Torre deveria ter movimentos disponíveis")

# ==================== FUNÇÃO PARA EXECUTAR OS TESTES ====================

def run_rook_tests():
    """Executa apenas os testes da Torre"""
    print("=" * 60)
    print("🧪 TESTANDO A TORRE")
    print("=" * 60)
    print()
    
    # Cria um suite com apenas os testes da Torre
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRook)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    print(f"📊 RESULTADO:")
    print(f"  ✅ Executados: {result.testsRun}")
    print(f"  ✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ❌ Falhas: {len(result.failures)}")
    print(f"  ⚠️  Erros: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    # Executa todos os testes
    unittest.main(verbosity=2)