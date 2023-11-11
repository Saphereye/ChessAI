import chess
from bots.base_bot import BaseBot
from bots.random_bot import RandomBot

bot1 = RandomBot()
bot2 = RandomBot()

board = chess.Board()

while not board.is_game_over():
    print("Bot 1")
    bot1_move = bot1.move(board)
    if bot1_move is None:
        print("No legal moves left")
        break
    board.push(bot1_move)
    print(board)
    print("Bot 2")
    bot2_move = bot2.move(board)
    if bot2_move is None:
        print("No legal moves left")
        break
    board.push(bot2_move)
    print(board)

print(f"{board.is_checkmate()=}")
print(f"{board.is_stalemate()=}")
print(f"{board.is_insufficient_material()=}")
print(f"""{"White" if board.turn else "Black"}""")
