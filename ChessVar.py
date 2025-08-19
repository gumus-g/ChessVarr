# Author: Gulper Gumus
# Github username: gumus-g
# Date: 12/10/2023
# Description: Create a class named ChessVar. Let this game create a list of chessboards.
#  And by following the chess moves, it is determined who won the game. All rules of the game
#  of chess should be applied here.White must make the first move and the one who captures all
#  of his opponent's pieces of the same type wins the game. You also need to keep track of whose
#  turn it is. Use method get_game_state and make_move.

class ChessVar:
    """
    Represent chessVar class.
    """

    def __init__(self):
        """
        Initialize the chess board and other data members
        """
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        self.whose_turn_is_it = 'white'
        self.game_state = 'UNFINISHED'

    def get_game_state(self):
        """
        A method called get_game_state that just returns
        'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'
        Input: No parameters
        :return:
        """
        return self.game_state

    def make_move(self, from_square, to_square):
        """
        Represents the square position it is moved to and
        the square position it is moved to.
        :param from_square:
        :param to_square:
        :return: False

       """
        # Check if the game is already finished
        if self.game_state != 'UNFINISHED':
            return False

        # Convert algebraic notation to board indices
        from_row, from_col = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
        to_row, to_col = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

        # Check if the move is legal and valid
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False

        # Make the move
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '

        # Check if the pieces are captured
        if self.board[to_row][to_col].islower():
            piece_type = self.board[to_row][to_col].upper()
            if all(piece != piece_type for row in self.board for piece in row):
                # All pieces of this type are captured, update game state
                self.game_state = 'WHITE_WON' if self.whose_turn_is_it == 'white' else 'BLACK_WON'

        # Update player turn
        self.whose_turn_is_it = 'black' if self.whose_turn_is_it == 'white' else 'white'

        return True

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """
        Checks is move is valid.
        :param from_row:
        :param from_col:
        :param to_row:
        :param to_col:
        :return:
        """
        # Check if the move is within the board range
        if not (0 <= from_row < 8) or not (0 <= from_col < 8) or not (0 <= to_row < 8) or not (0 <= to_col < 8):
            return False

        # Check if the piece belongs to the current player
        if (self.whose_turn_is_it == 'white' and not self.board[from_row][from_col].isupper()) or \
                (self.whose_turn_is_it == 'black' and not self.board[from_row][from_col].islower()):
            return False

        # Check for specific piece movement
        piece = self.board[from_row][from_col].lower()
        if piece == 'p':
            return self._get_pawn_moves(from_row, from_col, to_row, to_col)
        elif piece == 'n':
            return self._get_knight_moves(from_row, from_col, to_row, to_col)
        elif piece == 'b':
            return self._get_bishop_moves(from_row, from_col, to_row, to_col)
        elif piece == 'r':
            return self._get_rook_moves(from_row, from_col, to_row, to_col)
        elif piece == 'q':
            return self._get_queen_moves(from_row, from_col, to_row, to_col)
        elif piece == 'k':
            return self._get_king_moves(from_row, from_col, to_row, to_col)

        return True

    # def _is_winner(self, color):
    #     """
    #     Implements is_winner function.
    #     :param color:
    #     :return:
    #     """
    #     opponent_pieces = [piece.lower() for piece in sum(self.board, []) if piece.islower() != color.islower()]
    #     return all(piece == '' for piece in opponent_pieces)

    def _get_rook_moves(self, from_row, from_col, to_row, to_col):
        """
        Implements rook moves in row and column.
        :param from_row:
        :param from_col:
        :param to_row:
        :param to_col:
        :return:
        """
        return (from_row == to_row or from_col == to_col) and \
               self.is_clear_path(from_row, from_col, to_row, to_col)

    def _get_bishop_moves(self, from_row, from_col, to_row, to_col):
        """
        Implements bishop movement rules in row and column.
        :param from_row:
        :param from_col:
        :param to_row:
        :param to_col:
        :return:
        """
        return abs(from_row - to_row) == abs(from_col - to_col) and \
               self.is_clear_path(from_row, from_col, to_row, to_col)

    def _get_queen_moves(self, from_row, from_col, to_row, to_col):
        """
         Implements queen movement rules in row and column.
        :param from_row:
        :param from_col:
        :param to_row:
        :param to_col:
        :return:
        """
        return (from_row == to_row or from_col == to_col or
                abs(from_row - to_row) == abs(from_col - to_col)) and \
               self.is_clear_path(from_row, from_col, to_row, to_col)

    def _get_knight_moves(self, from_row, from_col, to_row, to_col):
        """
        Implements knight moves in row and column.
        :param from_row:
        :param from_col:
        :param to_row:
        :param to_col:
        :return:
        """
        return (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1) or \
               (abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2)

    def _get_pawn_moves(self, from_row, from_col, to_row, to_col):
        """
        Implements pawn moves in row and column.
        :param from_row:
        :param from_col:
        :return: moves
        """
        # Check pawn movement rules
        direction = 1 if self.whose_turn_is_it == 'white' else -1

        # Regular move
        if from_col == to_col and self.board[to_row][to_col] == ' ':
            if from_row + direction == to_row or (from_row == 1 and from_row + 2 * direction == to_row):
                return True

        # Capture move
        if abs(from_col - to_col) == 1 and from_row + direction == to_row:
            return self.board[to_row][to_col].islower() if direction == 1 else self.board[to_row][
                to_col].isupper()

        return False

    def _get_king_moves(self, from_row, from_col, to_row, to_col):
        """
        Implements king moves in row and column.
        :param from_row:
        :param from_col:
        :return: moves
        """
        return max(abs(from_row - to_row), abs(from_col - to_col)) == 1

    def is_clear_path(self, from_row, from_col, to_row, to_col):
        """
        Checks if the path between two squares is clear for pieces.
        :param from_row:
        :param from_col:
        :param to_row:
        :param to_col:
        :return: True
        """
        delta_row = 1 if to_row > from_row else -1 if to_row < from_row else 0
        delta_col = 1 if to_col > from_col else -1 if to_col < from_col else 0

        current_row, current_col = from_row + delta_row, from_col + delta_col
        while current_row != to_row or current_col != to_col:
            if self.board[current_row][current_col] != ' ':
                return False
            current_row += delta_row
            current_col += delta_col

        return True

