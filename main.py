import chess
from bots.random_bot import RandomBot
from bots.dfs_bot import DFSBot
from bots.helper import *
from chessboard import display

display_board = display.start()

# bot1 = DFSBot(max_depth=1)
bot1 = RandomBot()
# bot2 = DFSBot(max_depth=3)
bot2 = RandomBot()

board = chess.Board()

potential_winner = None

turn_number = 1

while True:
    print(f"Turn Number: {turn_number}")
    bot1_move = bot1.move(board)
    print(f"White moves: {bot1_move}")
    board.push(bot1_move)
    # print(board)
    display.update(board.fen(), display_board)
    print(f"Evaluation: {evaluate_board(board) : .2f}")

    if board.is_game_over():
        potential_winner = "White"
        break

    bot2_move = bot2.move(board)
    print(f"Black moves: {bot2_move}")
    board.push(bot2_move)
    # print(board)
    display.update(board.fen(), display_board)
    print(f"Evaluation: {evaluate_board(board) : .2f}")

    if board.is_game_over():
        potential_winner = "Black"
        break

    turn_number += 1

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
input()
