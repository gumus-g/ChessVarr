# Author: Gulper Gumus
# Github username: gumus-g
# Date: 12/10/2023
# Description: Create a class named ChessVar. Let this game create a list of chessboards.
#  And by following the chess moves, it is determined who won the game. All rules of the game
#  of chess should be applied here.White must make the first move and the one who captures all
#  of his opponent's pieces of the same type wins the game. You also need to keep track of whose
#  turn it is. Use method get_game_state and make_move.

class ChessVar:
    def __init__(self):
        """Initialize the board and game state."""
        self._board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self._current_turn = 'white'
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """Return current game state."""
        return self._game_state

    def make_move(self, from_square, to_square):
        """Attempt to move a piece. Return True if successful, False otherwise."""
        if self._game_state != 'UNFINISHED':
            return False

        from_row, from_col = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
        to_row, to_col = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

        if not self._is_valid_move(from_row, from_col, to_row, to_col):
            return False

        moving_piece = self._board[from_row][from_col]
        captured_piece = self._board[to_row][to_col]

        # Move the piece
        self._board[to_row][to_col] = moving_piece
        self._board[from_row][from_col] = ' '

        # Check win condition
        if captured_piece != ' ':
            captured_type = captured_piece.lower()
            captured_color = 'white' if captured_piece.isupper() else 'black'
            remaining = [p for row in self._board for p in row
                         if p.lower() == captured_type and
                         (p.isupper() if captured_color == 'white' else p.islower())]
            if not remaining:
                self._game_state = 'WHITE_WON' if self._current_turn == 'white' else 'BLACK_WON'

        # Switch turn
        self._current_turn = 'black' if self._current_turn == 'white' else 'white'
        return True

    def _is_valid_move(self, fr, fc, tr, tc):
        """Validate move based on piece type and turn."""
        if not (0 <= fr < 8 and 0 <= fc < 8 and 0 <= tr < 8 and 0 <= tc < 8):
            return False

        piece = self._board[fr][fc]
        if piece == ' ':
            return False

        if self._current_turn == 'white' and not piece.isupper():
            return False
        if self._current_turn == 'black' and not piece.islower():
            return False

        target = self._board[tr][tc]
        if target != ' ' and (piece.isupper() == target.isupper()):
            return False

        piece_type = piece.lower()
        if piece_type == 'p':
            return self._pawn_move(fr, fc, tr, tc)
        elif piece_type == 'n':
            return self._knight_move(fr, fc, tr, tc)
        elif piece_type == 'b':
            return self._bishop_move(fr, fc, tr, tc)
        elif piece_type == 'r':
            return self._rook_move(fr, fc, tr, tc)
        elif piece_type == 'q':
            return self._queen_move(fr, fc, tr, tc)
        elif piece_type == 'k':
            return self._king_move(fr, fc, tr, tc)

        return False

    def _pawn_move(self, fr, fc, tr, tc):
        direction = -1 if self._current_turn == 'white' else 1
        start_row = 6 if self._current_turn == 'white' else 1

        if fc == tc and self._board[tr][tc] == ' ':
            if tr == fr + direction:
                return True
            if fr == start_row and tr == fr + 2 * direction and self._board[fr + direction][fc] == ' ':
                return True
        elif abs(fc - tc) == 1 and tr == fr + direction:
            target = self._board[tr][tc]
            return target != ' ' and (target.isupper() != self._board[fr][fc].isupper())

        return False

    def _knight_move(self, fr, fc, tr, tc):
        return (abs(fr - tr), abs(fc - tc)) in [(2, 1), (1, 2)]

    def _bishop_move(self, fr, fc, tr, tc):
        return abs(fr - tr) == abs(fc - tc) and self._clear_path(fr, fc, tr, tc)

    def _rook_move(self, fr, fc, tr, tc):
        return (fr == tr or fc == tc) and self._clear_path(fr, fc, tr, tc)

    def _queen_move(self, fr, fc, tr, tc):
        return self._bishop_move(fr, fc, tr, tc) or self._rook_move(fr, fc, tr, tc)

    def _king_move(self, fr, fc, tr, tc):
        return max(abs(fr - tr), abs(fc - tc)) == 1

    def _clear_path(self, fr, fc, tr, tc):
        dr = (tr - fr) // max(1, abs(tr - fr)) if fr != tr else 0
        dc = (tc - fc) // max(1, abs(tc - fc)) if fc != tc else 0

        r, c = fr + dr, fc + dc
        while (r, c) != (tr, tc):
            if self._board[r][c] != ' ':
                return False
            r += dr
            c += dc
        return True

    def print_board(self):
        """Optional: Print board for debugging."""
        for row in self._board:
            print(' '.join(row))
        print()
