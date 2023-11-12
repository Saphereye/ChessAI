import chess
from bots.random_bot import RandomBot
from bots.dfs_bot import DFSBot

piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

def evaluate_board(board):
        evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.color == chess.WHITE:
                    evaluation += piece_values.get(piece.piece_type, 0)
                else:
                    evaluation -= piece_values.get(piece.piece_type, 0)

        return evaluation

bot1 = RandomBot()
# bot2 = DFSBot(max_depth=3)
bot2 = RandomBot()

board = chess.Board()

potential_winner = None

while True:
    print("Bot 1")
    bot1_move = bot1.move(board)
    print(f"White moves: {bot1_move}")
    board.push(bot1_move)
    print(board)
    print(f"Evaluation: {evaluate_board(board)}")

    if board.is_game_over():
        potential_winner = "White"
        break

    print("Bot 2")
    bot2_move = bot2.move(board)
    print(f"White moves: {bot2_move}")
    board.push(bot2_move)
    print(board)
    print(f"Evaluation: {evaluate_board(board)}")

    if board.is_game_over():
        potential_winner = "Black"
        break

if board.is_checkmate():
    print(f"{potential_winner} has won by checkmate")
elif board.is_stalemate():
    print("The game is a draw due to stalemate")
elif board.is_insufficient_material():
    print("The game is a draw due to insufficient material")
elif board.is_seventyfive_moves():
    print("The game is a draw due to the seventy-five move rule")
elif board.is_fivefold_repetition():
    print("The game is a draw due to fivefold repetition")
else:
    print("The game has ended for an unknown reason")

print(board)
