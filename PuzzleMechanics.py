import numpy as np


class SpaceOccupiedException(Exception):
    pass


class OutOfBoundsException(Exception):
    pass


class PuzzlePiece(object):
    def __init__(self, height, width, x, y, _id=None):
        """
        This class represents a single puzzle piece.

        x- and y- coordinates are the top left corner of object on the board
        array

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
        """
        This class represents a board, consisting of N x M fields in which
        puzzle pieces can be placed. This class allows the placement,
        movement, and removal of pieces and tests for the validity of these
        actions.

        It also keeps track of the "winning piece" and the goal
        position of this piece. These two properties can be set with the
        set_winning_piece() and set_goal() functions, respectively.
        Alternatively, static functions exist to make constructing a puzzle
        easier.

        :param height:
        :param width:
        """
        self._height = height
        self._width = width
        self._board = np.zeros(shape=(height, width), dtype=np.uint64)
        self._pieces = {}
        self._winning_piece_id = None
        self._goal_x = self._goal_y = None

    @staticmethod
    def create_puzzle(width, height, pieces, winning_id, goal_x, goal_y):
        """
        A helper function to create a complete puzzle.

        :param width:
        :param height:
        :param pieces: An iterable of PuzzlePiece objects or dictionaries with
        keys corresponding to the constructor of the PuzzlePiece function.
        Piece IDs are assigned by their order in the iterable.
        :param winning_id: The ID of the winning piece.
        :param goal_x: The x-coordinate the winning piece must reach
        :param goal_y: The y-coordinate the winning piece must reach
        :return:
        """
        board = PuzzleBoard(height=height, width=width)
        board.set_winning_piece(piece_id=winning_id)
        for pid, piece in enumerate(pieces):
            if not isinstance(piece, PuzzlePiece):
                piece = PuzzlePiece(_id=pid+1, **piece)
            board.add_piece(piece=piece)
        board.set_goal(x=goal_x, y=goal_y)

        # Check that the winning piece doesn't actually start on the goal
        winning_piece = board.get_winning_piece()
        if (winning_piece.get_x() == goal_x) and (winning_piece.get_y() == goal_y):
            raise ValueError("Trivial puzzle: winning piece is already on the goal")
        return board

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

    def get_winning_piece(self):
        return self._pieces[self._winning_piece_id]

    def set_winning_piece(self, piece_id):
        self._winning_piece_id = piece_id

    def get_goal(self):
        return self._goal_x, self._goal_y

    def set_goal(self, x, y):
        self._goal_x = x
        self._goal_y = y

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
            raise OutOfBoundsException("Puzzle piece is out of bounds")

        # Check that board is still empty at all positions
        if np.any(self._board[p_y_start:p_y_end, p_x_start:p_x_end] != 0):
            raise SpaceOccupiedException("Board is occupied at this position")

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
        Move a piece along the board. Checks that the move is permitted
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
            raise OutOfBoundsException("Puzzle piece cannot be moved out of bounds")

        # Check that no other piece is in the new positions
        new_location = self._board[
            p_y_start_new:p_y_end_new,
            p_x_start_new:p_x_end_new]
        if not np.all((new_location == 0) | (new_location == piece_id)):
            raise SpaceOccupiedException("Board is occupied at this position")

        self._board[p_y_start:p_y_end, p_x_start:p_x_end] = 0
        self._board[
            p_y_start_new:p_y_end_new,
            p_x_start_new:p_x_end_new] = piece_id
        self._pieces[piece_id].set_x(p_x_start_new)
        self._pieces[piece_id].set_y(p_y_start_new)

    def check_win(self):
        if (self.get_winning_piece().get_x() == self._goal_x) and \
           (self.get_winning_piece().get_y() == self._goal_y):
            return True
        return False
