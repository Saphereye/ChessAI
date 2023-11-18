import chess
import chess.engine
from chess import Move, Board
from bots.base_bot import BaseBot
import random

class StockfishBot(BaseBot):
    def __init__(self, engine_path: str = "./engines/stockfish-ubuntu-x86-64-avx2", time_limit: float = 0.5, depth: int = 5, skill_level: int = 0) -> None:
        super().__init__()
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        # min skill level 0, max skill level 20
        self.engine.configure({"Skill Level": skill_level})
        self.limit = chess.engine.Limit(time=time_limit)

    def move(self, board: Board) -> Move | None:
        return self.engine.play(board, self.limit).move