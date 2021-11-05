import unittest
from pieces import *

class TestRookPieces(unittest.TestCase):
    def test_rook_1(self):
        rook = Rook("a1", Color.WHITE)
        self.assertEqual(rook.move("a7"))


if __name__ == '__main__':
    unittest.main()