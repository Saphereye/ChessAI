import chess
from bots.random_bot import RandomBot
from bots.dfs_bot import GreedyDFSBot, FuzzyDFSBot, AlphaBetaBot, FuzzyPolyglotAlphaBetaBot, FuzzyAlphaBetaBot, IterativeDeepeningBot
from bots.quiescence_bot import QuiescenceBot
from bots.stockfish_bot import StockfishBot
from bots.helper import *
from chessboard import display
import matplotlib.pyplot as plt

def main():
    display_board = display.start()
    evaluation_list = []

    # bot1 = RandomBot()
    # bot1 = FuzzyPolyglotAlphaBetaBot(max_depth=3, book_path='./polyglot/Human.bin')
    # bot1 = FuzzyAlphaBetaBot(max_depth=3)
    bot1 = IterativeDeepeningBot(max_depth=3)
    # bot1 = FuzzyPolyglotAlphaBetaBot(max_depth=3, book_path='./polyglot/Titans.bin')
    bot2 = StockfishBot(engine_path="./engines/stockfish-ubuntu-x86-64-avx2", time_limit=0.1)
    # bot2 = FuzzyPolyglotAlphaBetaBot(max_depth=3, book_path='./polyglot/Human.bin')

    board = chess.Board()

    potential_winner = None

    turn_number = 1
    print(bot1, bot2)
    while True:
        print(f"Turn Number: {turn_number}")
        bot1_move = bot1.move(board)
        print(f"White moves: {bot1_move}")
        board.push(bot1_move)
        # print(board)
        display.update(board.fen(), display_board)
        evaluation = evaluate_board(board)
        evaluation_list.append(evaluation)
        print(f"Evaluation: {evaluation : .2f}")

        if board.is_game_over():
            potential_winner = "White"
            break

        bot2_move = bot2.move(board)
        print(f"Black moves: {bot2_move}")
        board.push(bot2_move)
        # print(board)
        display.update(board.fen(), display_board)
        evaluation = evaluate_board(board)
        evaluation_list.append(evaluation)
        print(f"Evaluation: {evaluation : .2f}")

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
    plt.plot([i+1 for i in range(len(evaluation_list))], evaluation_list)
    plt.show()

if __name__ == "__main__":
    main()
