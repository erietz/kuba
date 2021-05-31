import unittest
from KubaGame import KubaGame

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

if __name__ == '__main__':
    unittest.main()
