import chess
import chess.engine
from chess import Move, Board
from bots.base_bot import BaseBot
import random

class StockfishBot(BaseBot):
    def __init__(self, engine_path: str, time_limit: float = 0.5) -> None:
        super().__init__()
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.limit = chess.engine.Limit(time=time_limit)

    def move(self, board: Board) -> Move | None:
        return self.engine.play(board, self.limit).move