import chess
from chess import Move, Board
from bots.base_bot import BaseBot
from bots.helper import *
from bots.helper import Board
import random
import math

class QuiescenceBot(BaseBot):
    def __init__(self, max_depth: int = 3) -> None:
        self.max_depth = max_depth

    def move(self, board: Board) -> Move | None:
        legal_moves = list(board.legal_moves)
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in legal_moves:
            board.push(move)
            eval_score = self.alpha_beta(board, self.max_depth - 1, alpha, beta, False)
            board.pop()

            if eval_score > alpha:
                alpha = eval_score
                best_move = move

        return best_move

    def quiescence_search(self, board, alpha, beta):
        stand_pat = evaluate_board(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        legal_captures = [move for move in board.legal_moves if board.is_capture(move)]
        for move in legal_captures:
            board.push(move)
            score = -self.quiescence_search(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.quiescence_search(board, alpha, beta)

        legal_moves = list(board.legal_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
