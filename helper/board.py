from chess import *

class Board:
    def __init__(self) -> None:
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.is_white_turn = True
        self.move_history = []
    
    def make_move(self, move: Move):
        self.move_history.append(move)
        pass

    def undo_move(self, move: Move | None):
        if move is None:
            # undo last move
            pass
        else:
            pass

    def get_legal_moves(self):
        pass
    
    def is_in_check(self):
        pass

    def is_in_checkmate(self):
        pass
    
    def is_in_draw(self):
        # check for insufficient pieces also
        pass

    def draw_board(self):
        # https://www.alt-codes.net/chess-symbols.php
        pass
