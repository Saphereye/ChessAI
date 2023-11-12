import chess
from chess import Move, Board
from bots.base_bot import BaseBot

class DFSBot(BaseBot):
    def __init__(self, max_depth) -> None:
        self.max_depth = max_depth
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
    
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
            return self.evaluate_board(board)

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
    
    def evaluate_board(self, board) -> int:
        evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    evaluation += self.piece_values.get(piece.piece_type, 0)
                else:
                    evaluation -= self.piece_values.get(piece.piece_type, 0)

        return evaluation