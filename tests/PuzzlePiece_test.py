import unittest
import numpy as np
from PuzzleMechanics import PuzzleBoard, PuzzlePiece, \
    SpaceOccupiedException, OutOfBoundsException


class PuzzleBoardTest(unittest.TestCase):

    def test_create_board(self):
        board = PuzzleBoard(5, 5)
        np.testing.assert_array_equal(
            board.get_board(),
            np.zeros(shape=(5, 5), dtype=np.uint64))
        self.assertTrue(len(board.get_pieces()) == 0)

    def test_place_puzzle_piece(self):
        board = PuzzleBoard(5, 5)
        piece = PuzzlePiece(height=3, width=2, x=2, y=1, _id=5)
        board.add_piece(piece)
        np.testing.assert_array_equal(
            board.get_board(),
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 5, 5, 0],
                [0, 0, 5, 5, 0],
                [0, 0, 5, 5, 0],
                [0, 0, 0, 0, 0]],
                dtype=np.uint64))
        self.assertTrue(len(board.get_pieces()) == 1)

    def test_remove_piece(self):
        board = PuzzleBoard(5, 5)
        piece = PuzzlePiece(height=3, width=2, x=2, y=1, _id=20)
        board.add_piece(piece)
        board.remove_piece(piece_id=20)
        np.testing.assert_array_equal(
            board.get_board(),
            np.zeros(shape=(5, 5), dtype=np.uint64))
        self.assertTrue(len(board.get_pieces()) == 0)

    def test_move_piece(self):
        board = PuzzleBoard(5, 5)
        piece = PuzzlePiece(height=3, width=2, x=2, y=1, _id=1)
        board.add_piece(piece)
        board.move_piece(piece_id=1, delta_x=1, delta_y=1)
        np.testing.assert_array_equal(
            board.get_board(),
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1]],
                dtype=np.uint64))
        self.assertTrue(len(board.get_pieces()) == 1)

    def test_add_second_piece(self):
        board = PuzzleBoard(5, 5)
        piece = PuzzlePiece(height=3, width=2, x=3, y=2, _id=1)
        board.add_piece(piece)
        piece = PuzzlePiece(height=1, width=3, x=1, y=1, _id=2)
        board.add_piece(piece)
        np.testing.assert_array_equal(
            board.get_board(),
            np.array([
                [0, 0, 0, 0, 0],
                [0, 2, 2, 2, 0],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1]],
                dtype=np.uint64))
        self.assertTrue(len(board.get_pieces()) == 2)

    def test_move_piece_to_occupied_space(self):
        board = PuzzleBoard(5, 5)
        piece = PuzzlePiece(height=3, width=2, x=3, y=2, _id=1)
        board.add_piece(piece)
        piece = PuzzlePiece(height=1, width=3, x=1, y=1, _id=2)
        board.add_piece(piece)
        with self.assertRaises(SpaceOccupiedException):
            board.move_piece(piece_id=2, delta_x=1, delta_y=1)
        self.assertTrue(len(board.get_pieces()) == 2)

    def test_move_piece_out_of_bounds(self):
        board = PuzzleBoard(5, 5)
        piece = PuzzlePiece(height=3, width=2, x=3, y=2, _id=1)
        board.add_piece(piece)
        with self.assertRaises(OutOfBoundsException):
            board.move_piece(piece_id=1, delta_x=5, delta_y=5)
        self.assertTrue(len(board.get_pieces()) == 1)

    def test_static_creation_method(self):
        pieces = [
            {"x": 1, "y": 0, "width": 2, "height": 3},
            {"x": 1, "y": 4, "width": 4, "height": 1},
            {"x": 3, "y": 1, "width": 2, "height": 2}]
        board = PuzzleBoard.create_puzzle(
            width=5, height=5, pieces=pieces, winning_id=3, goal_x=2, goal_y=2)
        np.testing.assert_array_equal(
            board.get_board(),
            np.array([
                [0, 1, 1, 0, 0],
                [0, 1, 1, 3, 3],
                [0, 1, 1, 3, 3],
                [0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2]],
                dtype=np.uint64))
        self.assertEqual(len(board.get_pieces()), 3)
        self.assertEqual(board.get_goal(), (2, 2))
        self.assertEqual(board.get_winning_piece().get_x(), 3)
        self.assertEqual(board.get_winning_piece().get_y(), 1)
        self.assertEqual(board.get_winning_piece().get_width(), 2)
        self.assertEqual(board.get_winning_piece().get_height(), 2)
        self.assertEqual(board.get_winning_piece().get_id(), 3)

    def test_check_win(self):
        pieces = [{"x": 1, "y": 0, "width": 2, "height": 3}]
        board = PuzzleBoard.create_puzzle(
            width=5, height=5, pieces=pieces, winning_id=1, goal_x=2, goal_y=2)
        self.assertFalse(board.check_win())
        board.move_piece(piece_id=1, delta_x=1, delta_y=2)
        self.assertTrue(board.check_win())


if __name__ == '__main__':
    unittest.main()
