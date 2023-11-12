import chess
from chess import Move, Board

piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 200
        }

# Credits: Claude Shannon in 1949
def evaluate_board(board: Board) -> float:
    evaluation = 0
    if board.turn == chess.WHITE:
            evaluation += 0.1 * len(list(board.legal_moves))
            board.turn = chess.BLACK
            evaluation -= 0.1 * len(list(board.legal_moves))
            board.turn = chess.WHITE
    else:
            evaluation += 0.1 * len(list(board.legal_moves))
            board.turn = chess.WHITE
            evaluation -= 0.1 * len(list(board.legal_moves))
            board.turn = chess.BLACK
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                evaluation += piece_values.get(piece.piece_type, 0)
            else:
                evaluation -= piece_values.get(piece.piece_type, 0)

    return evaluation