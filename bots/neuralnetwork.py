import chess
from chess import Move, Board
from bots.base_bot import BaseBot
from bots.helper import *
from bots.helper import Board
import random
import math
import chess.polyglot
from keras.models import load_model
from bots.dfs_bot import FuzzyAlphaBetaBot
import numpy as np
import tensorflow as tf


class NNFuzzyPolyglotAlphaBetaBot(FuzzyAlphaBetaBot):
    def __init__(
        self,
        max_depth: int = 3,
        book_path: str = "./polyglot/Human.bin",
        model_path: str = "./neuralnetwork/size50k",
    ) -> None:
        super().__init__(max_depth)
        self.book = chess.polyglot.open_reader(book_path)
        self.model = load_model(filepath=model_path, compile=True)
        print(self.model.summary())

    def move(self, board: Board) -> Move | None:
        try:
            move = self.book.find(board).move
            # print(f"found in bin: {move}")
            return move
        except IndexError:
            pass

        possible_moves = []
        legal_moves = list(board.legal_moves)
        alpha = float("-inf")
        beta = float("inf")

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

    def fen_to_list(self, fen: str) -> list[int]:
        board = chess.Board(fen)
        #     print(board)
        output = []
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = piece.piece_type
                sign = 1 if piece.color == chess.WHITE else -1
                output.append(value * sign)
            else:
                output.append(0)
        return output

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return 1.0
            # return self.model.predict(self.fen_to_list(board.fen))

        legal_moves = list(board.legal_moves)

        if maximizing_player:
            max_eval = float("-inf")
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
            min_eval = float("inf")
            for move in legal_moves:
                board.push(move)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
