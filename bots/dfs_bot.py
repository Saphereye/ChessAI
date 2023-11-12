import chess
from chess import Move, Board
from bots.base_bot import BaseBot
from bots.helper import *

class DFSBot(BaseBot):
    def __init__(self, max_depth) -> None:
        self.max_depth = max_depth
    
    def move(self, board: Board) -> Move | None:
        legal_moves = list(board.legal_moves)
        best_move = None
        best_eval = float('-inf')

        for move in legal_moves:
            board.push(move)
            eval_score = self.dfs(board, self.max_depth - 1, False)
            board.pop()

            if eval_score > best_eval:
                best_eval = eval_score
                best_move = move

        return best_move
    
    def dfs(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        legal_moves = list(board.legal_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.dfs(board, depth - 1, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.dfs(board, depth - 1, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
            return min_eval