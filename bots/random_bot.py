import chess
from chess import Move, Board
from bots.base_bot import BaseBot
import random

class RandomBot(BaseBot):
    def move(self, board: Board) -> Move | None:
        legal_moves = list(board.legal_moves)
        if len(legal_moves) < 1:
            return None
        move = random.choice(list(board.legal_moves))
        print(move)
        return move