import chess
import chess.pgn
import random
import time
from math import log, sqrt, e, inf
from chessboard import display

class MonteCarloTreeSearch:
    def __init__(self):
        self.root = None

    class node():
        def __init__(self):
            self.state = chess.Board()
            self.action = ''
            self.children = set()
            self.parent = None
            self.N = 0
            self.n = 0
            self.v = 0

    def ucb1(curr_node):
        ans = curr_node.v + 2 * (sqrt(log(curr_node.N + e + (10 ** -6)) / (curr_node.n + (10 ** -10))))
        return ans

    def rollout(curr_node):
        if curr_node.state.is_game_over():
            board = curr_node.state
            if board.result() == '1-0':
                return 1, curr_node
            elif board.result() == '0-1':
                return -1, curr_node
            else:
                return 0.5, curr_node

        all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)]

        for i in all_moves:
            tmp_state = chess.Board(curr_node.state.fen())
            tmp_state.push_san(i)
            child = MonteCarloTreeSearch.node()
            child.state = tmp_state
            child.parent = curr_node
            curr_node.children.add(child)
        rnd_state = random.choice(list(curr_node.children))

        return MonteCarloTreeSearch.rollout(rnd_state)

    def expand(curr_node, white):
        if len(curr_node.children) == 0:
            return curr_node
        max_ucb = -inf
        if white:
            idx = -1
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = MonteCarloTreeSearch.ucb1(i)
                if tmp > max_ucb:
                    idx = i
                    max_ucb = tmp
                    sel_child = i

            return MonteCarloTreeSearch.expand(sel_child, 0)

        else:
            idx = -1
            min_ucb = inf
            sel_child = None
            for i in curr_node.children:
                tmp = MonteCarloTreeSearch.ucb1(i)
                if tmp < min_ucb:
                    idx = i
                    min_ucb = tmp
                    sel_child = i

            return MonteCarloTreeSearch.expand(sel_child, 1)

    def rollback(curr_node, reward):
        curr_node.n += 1
        curr_node.v += reward
        while curr_node.parent is not None:
            curr_node.N += 1
            curr_node = curr_node.parent
        return curr_node

    def mcts_pred(curr_node, over, white, iterations=10):
        if over:
            return -1
        all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)]
        map_state_move = dict()

        for i in all_moves:
            tmp_state = chess.Board(curr_node.state.fen())
            tmp_state.push_san(i)
            child = MonteCarloTreeSearch.node()
            child.state = tmp_state
            child.parent = curr_node
            curr_node.children.add(child)
            map_state_move[child] = i

        while iterations > 0:
            if white:
                idx = -1
                max_ucb = -inf
                sel_child = None
                for i in curr_node.children:
                    tmp = MonteCarloTreeSearch.ucb1(i)
                    if tmp > max_ucb:
                        idx = i
                        max_ucb = tmp
                        sel_child = i
                ex_child = MonteCarloTreeSearch.expand(sel_child, 0)
                reward, state = MonteCarloTreeSearch.rollout(ex_child)
                curr_node = MonteCarloTreeSearch.rollback(state, reward)
                iterations -= 1
            else:
                idx = -1
                min_ucb = inf
                sel_child = None
                for i in curr_node.children:
                    tmp = MonteCarloTreeSearch.ucb1(i)
                    if tmp < min_ucb:
                        idx = i
                        min_ucb = tmp
                        sel_child = i

                ex_child = MonteCarloTreeSearch.expand(sel_child, 1)

                reward, state = MonteCarloTreeSearch.rollout(ex_child)

                curr_node = MonteCarloTreeSearch.rollback(state, reward)
                iterations -= 1
        if white:

            mx = -inf
            idx = -1
            selected_move = ''
            for i in (curr_node.children):
                tmp = MonteCarloTreeSearch.ucb1(i)
                if tmp > mx:
                    mx = tmp
                    selected_move = map_state_move[i]
            return selected_move
        else:
            mn = inf
            idx = -1
            selected_move = ''
            for i in (curr_node.children):
                tmp = MonteCarloTreeSearch.ucb1(i)
                if tmp < mn:
                    mn = tmp
                    selected_move = map_state_move[i]
            return selected_move

    def move(self, board, turn):
        
        root = MonteCarloTreeSearch.node()
        root.state = board
        result = MonteCarloTreeSearch.mcts_pred(root, board.is_game_over(), turn)
        return result


'''def main():
    board = chess.Board()
    game_board = display.start()

    mcts = MonteCarloTreeSearch()

    moves = 0
    pgn = []
    game = chess.pgn.Game()
    evaluations = []
    sm = 0
    cnt = 0

    while not board.is_game_over():
        all_moves = [board.san(i) for i in list(board.legal_moves)]
        start = time.time()
        result = mcts.move(board, board.turn)
        sm += (time.time() - start)
        board.push_san(result)
        print(result)
        pgn.append(result)
        display.check_for_quit()
        display.update(board.fen(), game_board)

        moves += 1
        cnt += 1

    print("Average Time per move = ", sm / cnt)
    print(board)
    print(" ".join(pgn))
    print()
    print(board.result())
    game.headers["Result"] = board.result()
    print(game)


if __name__ == "__main__":
    main()'''
