import chess
from chess import Board

# Credits: Claude Shannon in 1949
def evaluate_board(board: Board):
    piece_counts = {
        chess.PAWN: [0, 0],
        chess.KNIGHT: [0, 0],
        chess.BISHOP: [0, 0],
        chess.ROOK: [0, 0],
        chess.QUEEN: [0, 0],
        chess.KING: [0, 0],
    }
    blocked_pawns = [0, 0]

    current_turn = board.turn

    board.turn = chess.WHITE
    white_legal_moves = list(board.legal_moves)
    board.turn = chess.BLACK
    black_legal_moves = list(board.legal_moves)

    board.turn = current_turn

    mobility = [0.1 * len(white_legal_moves), 0.1 * len(black_legal_moves)]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            color = 0 if piece.color == chess.WHITE else 1
            piece_type = piece.piece_type
            piece_counts[piece_type][color] += 1

            # Check for doubled, blocked, and isolated pawns
            if piece_type == chess.PAWN:
                if board.is_pinned(color, square):
                    blocked_pawns[color] += 1

    # Calculate the evaluation based on the provided formula
    evaluation = (
        200 * (piece_counts[chess.KING][0] - piece_counts[chess.KING][1])
        + 9 * (piece_counts[chess.QUEEN][0] - piece_counts[chess.QUEEN][1])
        + 5 * (piece_counts[chess.ROOK][0] - piece_counts[chess.ROOK][1])
        + 3
        * (
            piece_counts[chess.BISHOP][0] - piece_counts[chess.BISHOP][1]
            + piece_counts[chess.KNIGHT][0] - piece_counts[chess.KNIGHT][1]
        )
        + (piece_counts[chess.PAWN][0] - piece_counts[chess.PAWN][1])
        - 0.5 * (blocked_pawns[0] - blocked_pawns[1])
        + 0.1 * (mobility[0] - mobility[1])
    )

    return evaluation
