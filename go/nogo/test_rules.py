import unittest
from rules import legal_moves, play, groups_have_liberties

class NoGoTests(unittest.TestCase):
    def test_empty_board(self):
        self.assertEqual(legal_moves((0,) * 9, 1), list(range(9)))
        self.assertEqual(legal_moves((0,) * 9, 2), list(range(9)))

    def test_no_placement_on_occupied(self):
        board = (1,0,0,0,0,0,0,0,0)
        self.assertNotIn(0, legal_moves(board, 2))

    def test_suicide_prohibited(self):
        # Center is surrounded by white stones; black cannot play there.
        board = (0,2,0,2,0,2,0,2,0)
        self.assertNotIn(4, legal_moves(board, 1))

    def test_capture_prohibited(self):
        # Black at center has only liberty at index 7; white cannot fill it.
        board = (0,2,0,2,1,2,0,0,0)
        self.assertNotIn(7, legal_moves(board, 2))

    def test_legal_play(self):
        board = (0,) * 9
        after = play(board, 1, 4)
        self.assertEqual(after[4], 1)
        self.assertTrue(groups_have_liberties(after))

    def test_bad_board(self):
        with self.assertRaises(ValueError):
            legal_moves((0,0,0), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
