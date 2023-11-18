import chess
from chess import Move, Board
from bots.base_bot import BaseBot
import random

class RandomBot(BaseBot):
    def move(self, board: Board):
        return random.choice(list(board.legal_moves))