import numpy as np


class PuzzlePiece(object):
    """
    x- and y- coordinates are the top left corner of object on the board array
    """
    def __init__(self, height, width, x, y, _id=None):
        """
        :param height:
        :param width:
        :param x:
        :param y:
        :param _id:
        """
        self._height = height
        self._width = width
        self._x = x
        self._y = y
        if _id is None or _id < 1:
            _id = np.random.randint(
                low=1, high=np.iinfo(np.uint64).max, dtype=np.uint64)

        self._id = _id

    def __str__(self):
        return "PuzzlePiece: id={}, x={}, y={}, width={}, height={}".format(
            self._id, self._x, self._y, self._width, self._height)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_id(self):
        return self._id


class PuzzleBoard(object):
    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._board = np.zeros(shape=(height, width), dtype=np.uint64)
        self._pieces = {}

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_pieces(self):
        return self._pieces

    def get_piece(self, piece_id):
        return self._pieces[piece_id]

    def get_board(self):
        return self._board

    def add_piece(self, piece):
        """
        Add a piece to the board
        :param piece:
        :return:
        """
        # Check that ID doesn't already exist
        pid = piece.get_id()
        if pid in self._pieces.keys():
            raise ValueError("Piece ID already exists")

        p_x_start = piece.get_x()
        p_y_start = piece.get_y()
        p_x_end = p_x_start + piece.get_width()
        p_y_end = p_y_start + piece.get_height()

        # Check that piece is completely in-bounds
        if p_x_start < 0 or p_x_end > self._width or \
                p_y_start < 0 or p_y_end > self._height:
            raise ValueError("Puzzle piece is out of bounds")

        # Check that board is still empty at all positions
        if np.any(self._board[p_y_start:p_y_end, p_x_start:p_x_end] != 0):
            raise ValueError("Board is occupied at this position")

        self._board[p_y_start:p_y_end, p_x_start:p_x_end] = pid
        self._pieces[piece.get_id()] = piece

    def remove_piece(self, piece_id):
        """
        Removes a piece from the board
        :param piece_id:
        :return:
        """
        if piece_id not in self._pieces.keys():
            return None

        del self._pieces[piece_id]
        self._board[self._board == piece_id] = 0

    def move_piece(self, piece_id, delta_x, delta_y):
        """
        Move a piece along the board. Checks that the
        move is permitted
        :param piece_id:
        :param delta_x:
        :param delta_y:
        :return:
        """
        # Check that piece exists
        if piece_id not in self._pieces.keys():
            raise ValueError("Piece ID not recognized")

        # Get old coordinates
        piece = self._pieces[piece_id]
        p_x_start = piece.get_x()
        p_y_start = piece.get_y()
        p_x_end = p_x_start + piece.get_width()
        p_y_end = p_y_start + piece.get_height()

        # Set new coordinates
        p_x_start_new = p_x_start + delta_x
        p_x_end_new = p_x_end + delta_y
        p_y_start_new = p_y_start + delta_y
        p_y_end_new = p_y_end + delta_y

        # Check that new coords are completely in-bounds
        if p_x_start_new < 0 or p_x_end_new > self._width or \
                p_y_start_new < 0 or p_y_end_new > self._height:
            raise ValueError("Puzzle piece cannot be moved out of bounds")

        # Check that no other piece is in the new positions
        new_location = self._board[p_y_start_new:p_y_end_new, p_x_start_new:p_x_end_new]
        if not np.all((new_location == 0) | (new_location == piece_id)):
            raise ValueError("Board is occupied at this position")

        self._board[p_y_start:p_y_end, p_x_start:p_x_end] = 0
        self._board[p_y_start_new:p_y_end_new, p_x_start_new:p_x_end_new] = piece_id
        self._pieces[piece_id].set_x(p_x_start_new)
        self._pieces[piece_id].set_y(p_y_start_new)


def test_board():
    board = PuzzleBoard(5, 5)
    print(board.get_board())

    piece = PuzzlePiece(height=3, width=2, x=2, y=1, _id=1)
    board.add_piece(piece)
    print(board.get_board())

    piece = PuzzlePiece(height=1, width=2, x=0, y=0, _id=2)
    board.add_piece(piece)
    print(board.get_board())
    for piece in board.get_pieces():
        print(board.get_piece(piece))

    board.remove_piece(1)
    print(board.get_board())

    board.move_piece(piece_id=2, delta_x=1, delta_y=1)
    print(board.get_board())

    for piece in board.get_pieces():
        print(board.get_piece(piece))


test_board()
