import chess
from chess import Move, Board
from abc import ABC, abstractmethod

class BaseBot(ABC):
    @abstractmethod
    def move(self, board: Board):
        pass
