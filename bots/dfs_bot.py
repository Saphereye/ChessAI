import chess
from chess import Move, Board
from bots.base_bot import BaseBot
from bots.helper import *
from bots.helper import Board
import random
import math

class GreedyDFSBot(BaseBot):
    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth
        self.memo = {}
    
    def move(self, board: Board):
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

class FuzzyDFSBot(GreedyDFSBot):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)
    
    def move(self, board: Board):
        legal_moves = list(board.legal_moves)
        possible_moves = []

        for move in legal_moves:
            board.push(move)
            eval_score = self.dfs(board, self.max_depth - 1, False)
            board.pop()

            possible_moves.append((move, eval_score))
        sorted_moves = sorted(possible_moves, key=lambda x: x[1], reverse=True)
        weights = self.log_falloff_weights(len(sorted_moves))

        final_move = random.choices(population=sorted_moves, weights=weights)[0][0]
        # print(final_move)
        return final_move

    def log_falloff_weights(self, num_choices):
        # Generate logarithmic weights with a decreasing factor
        weights = [1 / (math.log2(i + 2)) for i in range(num_choices)]
        # Normalize weights to ensure they sum to 1
        total = sum(weights)
        normalized_weights = [w / total for w in weights]
        return normalized_weights

class AlphaBetaBot(GreedyDFSBot):
    def __init__(self, max_depth: int) -> None:
        super().__init__(max_depth)

    def move(self, board: Board):
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

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

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

class IterativeDeepeningBot(BaseBot):
    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth

    def move(self, board: Board):
        best_move = None
        for depth in range(1, self.max_depth + 1):
            print(f"Iterative Deepening: Depth {depth}")
            best_move = self.depth_limited_search(board, depth)
            if best_move is not None:
                break
        return best_move

    def depth_limited_search(self, board, depth):
        legal_moves = list(board.legal_moves)
        best_move = None
        best_eval = float('-inf')

        for move in legal_moves:
            board.push(move)
            eval_score = self.dfs(board, depth - 1, False)
            board.pop()

            if eval_score > best_eval:
                best_eval = eval_score
                best_move = move

        return best_move

    def dfs(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        legal_moves = list(board.legal_moves)

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.dfs(board, depth - 1, False)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self.dfs(board, depth - 1, True)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval



