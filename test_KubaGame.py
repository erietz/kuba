import unittest
from KubaGame import KubaGame

# TODO: Case where white knocks off all black balls and vice versa
# TODO: Case where there are no valid moves left for a player
# TODO: Case where the opponent cannot counteract a move indefinitely

class TestReadme(unittest.TestCase):

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
        self.assertTrue(game.make_move('ann', (0, 0), 'R'))
        self.assertTrue(game.make_move('bob', (6, 0), 'R'))
        self.assertTrue(game.make_move('ann', (0, 1), 'R'))
        self.assertTrue(game.make_move('bob', (6, 2), 'L'))
        self.assertTrue(game.make_move('ann', (0, 3), 'B'))
        game._display_board(colored=True)
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (1, 3), 'B'))
        self.assertTrue(game.get_captured('ann'), 1)
        self.assertTrue(game.make_move('ann', (2, 3), 'B'))
        self.assertTrue(game.get_captured('ann'), 2)
        self.assertTrue(game.make_move('ann', (3, 3), 'B'))
        self.assertTrue(game.get_captured('ann'), 3)
        self.assertTrue(game.make_move('ann', (4, 3), 'B'))
        self.assertTrue(game.get_captured('ann'), 4)
        self.assertTrue(game.make_move('ann', (5, 3), 'B'))
        self.assertTrue(game.get_captured('ann'), 5)
        self.assertTrue(game.make_move('ann', (1, 0), 'R'))
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertTrue(game.make_move('ann', (0, 2), 'B'))
        self.assertTrue(game.make_move('bob', (6, 0), 'F'))
        self.assertTrue(game.make_move('ann', (1, 2), 'B'))
        self.assertTrue(game.make_move('bob', (4, 0), 'B'))
        self.assertTrue(game.make_move('ann', (2, 2), 'B'))
        self.assertEqual(game.get_winner(), None)
        self.assertTrue(game.make_move('ann', (3, 2), 'B'))
        self.assertEqual(game.get_winner(), 'ann')

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
