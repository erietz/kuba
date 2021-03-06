# Author      : Ethan Rietz
# Date        : 2021-06-09
# Description : Unittests for the KubaGame.py file. Run using make test.

import unittest
from KubaGame import KubaGame, KubaBoard, KubaPlayer

class testKubaBoard(unittest.TestCase):
    def test_clone(self):
        original_board = [ ['R' for _ in range(7)] for _ in range(7) ]
        board = KubaBoard()
        cloned_board = KubaBoard(original_board)
        self.assertNotEqual(board.board, original_board)
        self.assertEqual(original_board, cloned_board.board)

        original_board = [ [' ' for _ in range(7)] for _ in range(7) ]
        cloned_board = KubaBoard(original_board)
        self.assertEqual(original_board, cloned_board.board)

    def test_marble_count(self):
        board = KubaBoard()
        self.assertEqual(board.get_marble_count(), (8, 8, 13))

    def test_get_marble(self):
        board = KubaBoard()
        self.assertEqual(board.get_marble((0, 0)), 'W')
        self.assertEqual(board.get_marble((3, 0)), 'X')
        self.assertEqual(board.get_marble((3, 1)), 'R')
        self.assertEqual(board.get_marble((3, 5)), 'R')
        self.assertEqual(board.get_marble((3, 6)), 'X')
        self.assertEqual(board.get_marble((6, 5)), 'W')
        self.assertEqual(board.get_marble((6, 6)), 'W')
        self.assertEqual(board.get_marble((6, 0)), 'B')
        self.assertEqual(board.get_marble((5, 1)), 'B')

class TestKubaPlayer(unittest.TestCase):
    def test_player(self):
        p1 = KubaPlayer(('ethan', 'B'))
        self.assertEqual(p1.get_name(), 'ethan')
        self.assertEqual(p1.get_color(), 'B')
        self.assertEqual(p1.get_captured_count(), 0)
        self.assertIsNone(p1.increment_captured_count())
        self.assertEqual(p1.get_captured_count(), 1)

class TestKubaGame(unittest.TestCase):

    def test_readme_example(self):
        game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
        self.assertEqual(game.get_marble_count(), (8,8,13))
        self.assertEqual(game.get_captured('PlayerA'), 0)
        self.assertIsNone(game.get_current_turn())
        self.assertIsNone(game.get_winner())
        self.assertTrue(game.make_move('PlayerA', (6,5), 'F'))
        self.assertEqual(game.get_current_turn(), 'PlayerB') # because PlayerA has just played.
        self.assertFalse(game.make_move('PlayerA', (6,5), 'L'))
        self.assertEqual(game.get_marble((5,5)), 'W')

    def test_easiest_win(self):
        game = KubaGame(('ann', 'W'), ('bob', 'B'))
        #game._debug = True
        #game._debug_color = True
        self.assertTrue(game.make_move('ann', (0, 0), 'R'))
        self.assertTrue(game.make_move('bob', (6, 0), 'R'))
        self.assertTrue(game.make_move('ann', (0, 1), 'R'))
        self.assertTrue(game.make_move('bob', (6, 2), 'L'))
        self.assertTrue(game.make_move('ann', (0, 3), 'B'))
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (1, 3), 'B'))
        self.assertEqual(game.get_captured('ann'), 1)
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertTrue(game.make_move('ann', (2, 3), 'B'))
        self.assertEqual(game.get_captured('ann'), 2)
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (3, 3), 'B'))
        self.assertEqual(game.get_captured('ann'), 3)
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertTrue(game.make_move('ann', (4, 3), 'B'))
        self.assertEqual(game.get_captured('ann'), 4)
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (5, 3), 'B'))
        self.assertEqual(game.get_captured('ann'), 5)
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertTrue(game.make_move('ann', (5, 6), 'L'))
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (5, 4), 'F'))
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertTrue(game.make_move('ann', (4, 4), 'F'))
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (3, 4), 'F'))
        self.assertEqual(game.get_captured('ann'), 6)
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertEqual(game.get_winner(), None)
        self.assertTrue(game.make_move('ann', (2, 4), 'F'))
        self.assertEqual(game.get_captured('ann'), 7)
        self.assertEqual(game.get_winner(), 'ann')
        self.assertFalse(game.make_move('bob', (6, 0), 'F'))
        self.assertFalse(game.make_move('ann', (1, 0), 'R'))

    def test_bob_wins_by_killing_ann(self):
        game = KubaGame(('ann', 'W'), ('bob', 'B'))
        game._debug = True
        game._debug_color = True
        game._board.display(colored=True)
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (0, 0), 'B'))
        self.assertTrue(game.make_move('bob', (5, 0), 'F'))
        self.assertTrue(game.make_move('ann', (0, 1), 'B'))
        self.assertTrue(game.make_move('bob', (4, 0), 'F'))
        self.assertTrue(game.make_move('ann', (1, 1), 'B'))
        self.assertTrue(game.make_move('bob', (3, 0), 'F'))
        self.assertEqual(game.get_marble_count(), (7,8,13))
        self.assertTrue(game.make_move('ann', (6, 6), 'F'))
        self.assertTrue(game.make_move('bob', (2, 0), 'F'))
        self.assertEqual(game.get_marble_count(), (6,8,13))
        self.assertTrue(game.make_move('ann', (4, 6), 'B'))
        self.assertTrue(game.make_move('bob', (6, 1), 'F'))
        self.assertTrue(game.make_move('ann', (6, 6), 'F'))
        self.assertTrue(game.make_move('bob', (5, 1), 'F'))
        self.assertTrue(game.make_move('ann', (4, 6), 'B'))
        self.assertTrue(game.make_move('bob', (4, 1), 'F'))
        self.assertEqual(game.get_marble_count(), (5,8,13))
        self.assertTrue(game.make_move('ann', (6, 6), 'F'))
        self.assertTrue(game.make_move('bob', (3, 1), 'F'))
        self.assertEqual(game.get_marble_count(), (4,8,13))
        self.assertTrue(game.make_move('ann', (4, 6), 'B'))
        self.assertTrue(game.make_move('bob', (0, 6), 'B'))
        self.assertTrue(game.make_move('ann', (6, 6), 'F'))
        self.assertTrue(game.make_move('bob', (1, 6), 'B'))
        self.assertTrue(game.make_move('ann', (6, 5), 'F'))
        self.assertTrue(game.make_move('bob', (2, 6), 'B'))
        self.assertTrue(game.make_move('ann', (5, 5), 'F'))
        self.assertTrue(game.make_move('bob', (3, 6), 'B'))
        self.assertEqual(game.get_marble_count(), (3,8,13))
        self.assertTrue(game.make_move('ann', (4, 5), 'F'))
        self.assertEqual(game.get_marble_count(), (3,7,13))
        self.assertTrue(game.make_move('bob', (0, 5), 'B'))
        self.assertTrue(game.make_move('ann', (6, 6), 'F'))
        self.assertTrue(game.make_move('bob', (1, 5), 'B'))
        self.assertTrue(game.make_move('ann', (5, 6), 'F'))
        self.assertTrue(game.make_move('bob', (2, 5), 'B'))
        self.assertTrue(game.make_move('ann', (4, 6), 'F'))
        self.assertTrue(game.make_move('bob', (3, 5), 'B'))
        self.assertTrue(game.make_move('ann', (6, 5), 'F'))
        self.assertTrue(game.make_move('bob', (1, 6), 'B'))
        self.assertTrue(game.make_move('ann', (4, 6), 'L'))
        self.assertTrue(game.make_move('bob', (3, 5), 'B'))
        self.assertTrue(game.make_move('ann', (6, 5), 'R'))
        self.assertTrue(game.make_move('bob', (4, 5), 'B'))
        self.assertTrue(game.make_move('ann', (6, 6), 'F'))
        self.assertTrue(game.make_move('bob', (2, 6), 'B'))
        self.assertTrue(game.make_move('ann', (6, 5), 'F'))
        self.assertTrue(game.make_move('bob', (3, 6), 'B'))
        self.assertTrue(game.make_move('ann', (5, 5), 'F'))
        self.assertTrue(game.make_move('bob', (4, 6), 'B'))
        self.assertTrue(game.make_move('ann', (4, 5), 'F'))
        self.assertTrue(game.make_move('bob', (0, 0), 'B'))
        self.assertTrue(game.make_move('ann', (3, 5), 'F'))
        self.assertTrue(game.make_move('bob', (2, 0), 'R'))
        self.assertTrue(game.make_move('ann', (2, 6), 'F'))
        self.assertTrue(game.make_move('bob', (1, 5), 'R'))
        self.assertEqual(game.get_marble_count(), (0,7,13))
        self.assertEqual(game.get_winner(), 'bob')

    def test_ann_wins_by_killing_bob(self):
        game = KubaGame(('ann', 'W'), ('bob', 'B'))
        #game._debug = True
        #game._debug_color = True
        #game._board.display(colored=True)
        self.assertTrue(game.make_move('ann', (0,0), 'B'))
        self.assertTrue(game.make_move('bob', (0,6), 'B'))
        self.assertTrue(game.make_move('ann', (1,0), 'B'))
        self.assertTrue(game.make_move('bob', (1,6), 'B'))
        self.assertTrue(game.make_move('ann', (3,0), 'R'))
        self.assertEqual(game.get_marble_count(), (8,7,13))
        self.assertTrue(game.make_move('bob', (2,6), 'B'))
        self.assertTrue(game.make_move('ann', (3,1), 'R'))
        self.assertEqual(game.get_marble_count(), (8,6,13))
        self.assertTrue(game.make_move('bob', (6,1), 'F'))
        self.assertTrue(game.make_move('ann', (6,6), 'F'))
        self.assertTrue(game.make_move('bob', (5,1), 'F'))
        self.assertTrue(game.make_move('ann', (5,6), 'F'))
        self.assertTrue(game.make_move('bob', (6,0), 'F'))
        self.assertTrue(game.make_move('ann', (3,6), 'L'))
        self.assertTrue(game.make_move('bob', (4,1), 'F'))
        self.assertTrue(game.make_move('ann', (3,5), 'L'))
        self.assertEqual(game.get_marble_count(), (8,5,13))
        self.assertTrue(game.make_move('bob', (0,5), 'B'))
        self.assertTrue(game.make_move('ann', (3,4), 'L'))
        self.assertEqual(game.get_marble_count(), (8,4,13))
        self.assertTrue(game.make_move('bob', (5,0), 'F'))
        self.assertTrue(game.make_move('ann', (3,3), 'L'))
        self.assertEqual(game.get_marble_count(), (8,3,13))
        self.assertTrue(game.make_move('bob', (4,0), 'F'))
        self.assertTrue(game.make_move('ann', (3,2), 'L'))
        self.assertEqual(game.get_marble_count(), (8,2,13))
        self.assertTrue(game.make_move('bob', (2,5), 'F'))
        self.assertTrue(game.make_move('ann', (0,0), 'B'))
        self.assertTrue(game.make_move('bob', (0,5), 'B'))
        self.assertTrue(game.make_move('ann', (1,0), 'B'))
        self.assertTrue(game.make_move('bob', (1,5), 'B'))
        self.assertTrue(game.make_move('ann', (2,0), 'R'))
        self.assertTrue(game.make_move('bob', (3,5), 'R'))
        self.assertTrue(game.make_move('ann', (2,1), 'R'))
        self.assertEqual(game.get_marble_count(), (8,1,12))
        self.assertTrue(game.make_move('bob', (3,6), 'L'))
        self.assertTrue(game.make_move('ann', (6,5), 'F'))
        self.assertTrue(game.make_move('bob', (3,5), 'R'))
        self.assertTrue(game.make_move('ann', (4,6), 'F'))
        self.assertTrue(game.make_move('bob', (2,6), 'L'))
        #self.assertTrue(game.make_move('ann', (5,5), 'F'))
        self.assertTrue(game.make_move('ann', (3,6), 'B'))
        self.assertTrue(game.make_move('bob', (2,5), 'B'))
        self.assertTrue(game.make_move('ann', (4,6), 'B'))
        self.assertTrue(game.make_move('bob', (3,5), 'R'))
        self.assertTrue(game.make_move('ann', (2,1), 'R'))
        self.assertTrue(game.make_move('bob', (3,6), 'F'))
        self.assertTrue(game.make_move('ann', (2,2), 'R'))
        self.assertEqual(game.get_marble_count(), (8,0,12))
        self.assertEqual(game.get_winner(), 'ann')

    def test_cant_undo_move(self):
        game = KubaGame(('ann', 'W'), ('bob', 'B'))
        #game._debug = True
        #game._debug_color = True
        #game._board.display(colored=True)
        self.assertTrue(game.make_move('ann', (0,0), 'B'))
        self.assertTrue(game.make_move('bob', (6,0), 'F'))
        self.assertTrue(game.make_move('ann', (1,0), 'B'))
        self.assertTrue(game.make_move('bob', (5,0), 'F'))
        self.assertFalse(game.make_move('ann', (1,0), 'B'))
        self.assertTrue(game.make_move('ann', (6,6), 'F'))
        self.assertTrue(game.make_move('bob', (0,6), 'B'))
        self.assertTrue(game.make_move('ann', (5,6), 'F'))
        self.assertTrue(game.make_move('bob', (1,6), 'B'))
        self.assertFalse(game.make_move('ann', (5,6), 'F'))
        self.assertTrue(game.make_move('ann', (6,5), 'F'))
        self.assertTrue(game.make_move('bob', (0,5), 'B'))
        self.assertTrue(game.make_move('ann', (5,6), 'F'))
        self.assertTrue(game.make_move('bob', (3,0), 'R'))
        self.assertTrue(game.make_move('ann', (4,6), 'F'))
        self.assertTrue(game.make_move('bob', (1,5), 'B'))
        self.assertTrue(game.make_move('ann', (3,6), 'L'))
        self.assertFalse(game.make_move('bob', (3,0), 'R'))

    def test_transpose_matrix(self):
        game = KubaGame(('ann', 'W'), ('bob', 'B'))
        matrix = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        new_matrix = [
            [1, 3, 5],
            [2, 4, 6]
        ]

        self.assertEqual(new_matrix, game._transpose_matrix(matrix))
        self.assertEqual(game._transpose_matrix(new_matrix), matrix)

        matrix = [
            [1, 2, 3],
            [3, 4, 5],
            [7, 8, 9]
        ]
        new_matrix = [
            [1, 3, 7],
            [2, 4, 8],
            [3, 5, 9]
        ]
        self.assertEqual(new_matrix, game._transpose_matrix(matrix))
        self.assertEqual(game._transpose_matrix(new_matrix), matrix)


if __name__ == '__main__':
    unittest.main()
