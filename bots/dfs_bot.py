import chess
from chess import Move, Board
from bots.base_bot import BaseBot
from bots.helper import *
from bots.helper import Board
import random
import math
import chess.polyglot

class GreedyDFSBot(BaseBot):
    def __init__(self, max_depth: int = 2) -> None:
        self.max_depth = max_depth
        self.memo = {}
    
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

class FuzzyDFSBot(GreedyDFSBot):
    def __init__(self, max_depth: int = 2) -> None:
        super().__init__(max_depth)
    
    def move(self, board: Board) -> Move | None:
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
    def __init__(self, max_depth: int = 3) -> None:
        super().__init__(max_depth)

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

class FuzzyAlphaBetaBot(AlphaBetaBot, FuzzyDFSBot):
   def __init__(self, max_depth: int = 3) -> None:
       super().__init__(max_depth)

   def move(self, board: Board) -> Move | None:
        possible_moves = []
        legal_moves = list(board.legal_moves)
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in legal_moves:
            board.push(move)
            eval_score = self.alpha_beta(board, self.max_depth - 1, alpha, beta, False)
            board.pop()

            possible_moves.append((move, eval_score))

            if eval_score > alpha:
                alpha = eval_score

        sorted_moves = sorted(possible_moves, key=lambda x: x[1], reverse=True)
        weights = self.log_falloff_weights(len(sorted_moves))

        final_move = random.choices(population=sorted_moves, weights=weights)[0][0]
        return final_move


class FuzzyPolyglotAlphaBetaBot(FuzzyAlphaBetaBot):
    def __init__(self, max_depth: int = 3, book_path: str = './polyglot/Human.bin') -> None:
        self.book = chess.polyglot.open_reader(book_path)
        super().__init__(max_depth)

    def move(self, board: Board) -> Move | None:
        try:
            move = self.book.find(board).move
            # print(f"found in bin: {move}")
            return move
        except IndexError:
            pass

        possible_moves = []
        legal_moves = list(board.legal_moves)
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in legal_moves:
            board.push(move)
            eval_score = self.alpha_beta(board, self.max_depth - 1, alpha, beta, False)
            board.pop()

            possible_moves.append((move, eval_score))

            if eval_score > alpha:
                alpha = eval_score

        sorted_moves = sorted(possible_moves, key=lambda x: x[1], reverse=True)
        weights = self.log_falloff_weights(len(sorted_moves))

        final_move = random.choices(population=sorted_moves, weights=weights)[0][0]
        return final_move

class NegamaxBot(BaseBot):
    def __init__(self, max_depth: int = 3) -> None:
        self.max_depth = max_depth
    
    def move(self, board: Board) -> Move | None:
        legal_moves = list(board.legal_moves)
        best_move = None
        best_eval = float('-inf')

        for move in legal_moves:
            board.push(move)
            eval_score = -self.negamax(board, self.max_depth - 1)
            board.pop()

            if eval_score > best_eval:
                best_eval = eval_score
                best_move = move

        return best_move
    
    def negamax(self, board, depth):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        legal_moves = list(board.legal_moves)
        max_eval = float('-inf')

        for move in legal_moves:
            board.push(move)
            eval_score = -self.negamax(board, depth - 1)
            board.pop()
            max_eval = max(max_eval, eval_score)
        
        return max_eval