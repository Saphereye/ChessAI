import chess
from bots.random_bot import RandomBot
from bots.dfs_bot import DFSBot

bot1 = RandomBot()
bot2 = DFSBot(max_depth=3)

board = chess.Board()

potential_winner = None

while True:
    print("Bot 1")
    bot1_move = bot1.move(board)
    board.push(bot1_move)
    print(board)

    if board.is_game_over():
        potential_winner = "White"
        break

    print("Bot 2")
    bot2_move = bot2.move(board)
    board.push(bot2_move)
    print(board)

    if board.is_game_over():
        potential_winner = "Black"
        break

if board.is_checkmate():
    print(f"{potential_winner} has won")
else:
    print(f"{board.is_stalemate()=}")
    print(f"{board.is_insufficient_material()=}")
print(board)
