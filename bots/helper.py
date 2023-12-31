import chess
from chess import Board

pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}

def evaluate_board(board: Board):
    evaluation = 0.0
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

    if board.is_check:
        evaluation -= 10.0
    else:
        if board.gives_check:
            evaluation += 10.0
        elif board.is_checkmate:
            evaluation += 20.0

    mobility = [0.1 * len(white_legal_moves), 0.1 * len(black_legal_moves)]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            color = 0 if piece.color == chess.WHITE else 1
            piece_type = piece.piece_type
            piece_counts[piece_type][color] += 1
            evaluation += pst[piece_type][square]

            # Check for doubled, blocked, and isolated pawns
            if piece_type == chess.PAWN:
                if board.is_pinned(color, square):
                    blocked_pawns[color] += 1

    # Calculate the evaluation based on the provided formula
    evaluation = (
        60000 * (piece_counts[chess.KING][0] - piece_counts[chess.KING][1])
        + 929 * (piece_counts[chess.QUEEN][0] - piece_counts[chess.QUEEN][1])
        + 479 * (piece_counts[chess.ROOK][0] - piece_counts[chess.ROOK][1])
        + 320 * (piece_counts[chess.BISHOP][0] - piece_counts[chess.BISHOP][1])
        + 280 * (piece_counts[chess.KNIGHT][0] - piece_counts[chess.KNIGHT][1])
        + 100 * (piece_counts[chess.PAWN][0] - piece_counts[chess.PAWN][1])
        - 100 * (blocked_pawns[0] - blocked_pawns[1])
        + 10 * (mobility[0] - mobility[1])
    )

    # if board.is_check():
    #     evaluation += 20 * (1 if board.turn == chess.BLACK else -1)

    return evaluation
