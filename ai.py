import copy
import datetime
import random


class State:
    def __init__(self, board, myColor, turn, step=None, round=1):
        self.board = board
        self.myColor = myColor      # 1: black, 2: white
        self.otherColor = 3 - myColor
        self.turn = turn            # 'me', 'other'
        self.step = step            # [i, j]
        self.round = round
        self.pieceNum = self.count_pieces()
        self.score = self.judge_board()
        self.minMax = self.score
        self.children = []

    def judge_board(self):
        score_board = [[ 100, -30,  20,  -5,  -5,  20, -30, 100],
                       [ -30, -70, -20, -15, -15, -20, -70, -30],
                       [  20, -20,  10,  10,  10,  10, -20,  20],
                       [  -5, -15,  10,   5,   5,  10, -15,  -5],
                       [  -5, -15,  10,   5,   5,  10, -15,  -5],
                       [  20, -20,  10,  10,  10,  10, -20,  20],
                       [ -30, -70, -20, -15, -15, -20, -70, -30],
                       [ 100, -30,  20,  -5,  -5,  20, -30, 100]]
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.myColor:
                    score += score_board[i][j]
                elif self.board[i][j] == self.otherColor:
                    score -= score_board[i][j]
        return score

    def count_pieces(self):
        pieceNum = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    pieceNum += 1
        return pieceNum

    def search_next_step(self):
        directionBox = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        turnColor = 1 if ([self.myColor, self.turn] in [[1, 'me'], [2, 'other']]) else 2
        byeColor = 3 - turnColor

        stepBox = []
        for boardx in range(8):
            for boardy in range(8):
                board = copy.deepcopy(self.board)
                feasible = False
                if self.board[boardx][boardy] == 0:
                    for direction in directionBox:
                        i = 1
                        while True:
                            nextScanfx = boardx + i * direction[0]
                            nextScanfy = boardy + i * direction[1]
                            if (nextScanfx in range(8)) and (nextScanfy in range(8)):
                                if board[nextScanfx][nextScanfy] == byeColor:
                                    i += 1
                                elif board[nextScanfx][nextScanfy] == turnColor:
                                    if i > 1:
                                        feasible = True
                                        for j in range(i):
                                            board[boardx + j * direction[0]][boardy + j * direction[1]] = turnColor
                                    break
                                else:
                                    break
                            else:
                                break
                if feasible:
                    stepBox.append({'step': [boardx, boardy], 'board': board})
        if stepBox != []:
            for step in stepBox:
                self.children.append(State(step['board'], self.myColor, self.next_turn(), step['step'], self.round+1))
        else:
            self.children.append(State(self.board, self.myColor, self.next_turn(), None, self.round+1))
        return stepBox

    def next_turn(self):
        if self.turn == 'me':
            return 'other'
        else:
            return 'me'


def initial_board():
    board = []
    for i in range(8):
        line = []
        for j in range(8):
            line.append(0)
        board.append(line)
    board[3][4] = board[4][3] = 1
    board[3][3] = board[4][4] = 2
    return board


def deep_search(state, depth_arrived, depth):
    if depth_arrived < depth:
        if state.children == []:
            state.search_next_step()
        for child in state.children:
            deep_search(child, depth_arrived+1, depth)
            # print(child.round, child.score, child.minMax, child.board)
        if state.turn == 'me':
            state.minMax = max([child.minMax for child in state.children])
        else:
            state.minMax = min([child.minMax for child in state.children])
        # print(state.round, state.score, state.minMax, state.board)
    if depth_arrived == 0:
        step = random.choice([child.step for child in state.children if child.minMax == state.minMax])
        return step, state.minMax


# board = initial_board()
board = [[ 2, 2, 2, 2, 2, 2, 2, 2],
         [ 2, 2, 2, 2, 2, 2, 2, 2],
         [ 2, 2, 2, 1, 1, 2, 2, 2],
         [ 2, 2, 2, 2, 2, 1, 2, 2],
         [ 2, 2, 2, 2, 2, 2, 1, 2],
         [ 2, 2, 1, 1, 1, 1, 2, 2],
         [ 2, 2, 2, 2, 2, 2, 2, 2],
         [ 2, 2, 2, 2, 2, 2, 2, 1]]
state = State(board, 1, 'me')
print(deep_search(state, 0, 5))



