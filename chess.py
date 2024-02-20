import numpy as np


class Game:

    def __init__(self):
        self.board = [
            ['br1', 'bn1', 'bb1', 'bq', 'bk', 'bb2', 'bn2', 'br2'],
            ['a7p', 'b7p', 'c7p', 'd7p', 'e7p', 'f7p', 'g7p', 'h7p'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
            ['wr1', 'wn1', 'wb1', 'wq', 'wk', 'wb2', 'wn2', 'wr2']
        ]
        self.moved = {
            'a2p': False, 'b2p': False, 'c2p': False, 'd2p': False,
            'e2p': False, 'f2p': False, 'g2p': False, 'h2p': False,
            'a7p': False, 'b7p': False, 'c7p': False, 'd7p': False,
            'e7p': False, 'f7p': False, 'g7p': False, 'h7p': False,
            'wk': False, 'wr1': False, 'br1': False, 'br2': False
        }
    def Player_Turn(self):

        move = str(input('move'))
        moved = self.moved[move]
        turn1 = Pieces(7, 4, moved, 'w', self.board)
        print(turn1.king())



class Pieces:

    def __init__(self, x_coordinate: int, y_coordinate: int, moved: dict, color: str, board) -> None:

        self.BOARD_SIZE = 8
        self.BOARD = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
        self.color = color
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.moved = moved
        self.possible_moves = []

        self.board = np.array(board)
        array_position = np.where(self.board != '_')
        rows, cols = array_position[0], array_position[1]
        self.occupied_squares = list(zip(rows, cols))

    def pawn(self) -> list:

        self.possible_moves.append([self.x_coordinate+1, self.y_coordinate])
        if not self.moved:
            self.possible_moves.append([self.x_coordinate+2, self.y_coordinate])

        self.possible_moves = [x for x in self.possible_moves if x not in self.occupied_squares]
        return self.possible_moves


    def knight(self) -> list:
        '''
        The knight cannot be blocked so we do not need to check where it can move apart from the restrictions of the
        board width.
        :return: List of possible moves for the knight given a starting point
        '''
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:

                if (abs(dx) == 1 == abs(dy) == 1) or (abs(dx) == 2 == abs(dy) == 2):
                    continue
                if 0 <= self.x_coordinate + dx < self.BOARD_SIZE or 0 <= self.y_coordinate + dy < self.BOARD_SIZE:
                    self.possible_moves.append([self.x_coordinate + dx, self.y_coordinate + dy])

        self.possible_moves = [x for x in self.possible_moves if x not in self.occupied_squares]
        return self.possible_moves

    def bishop(self) -> list:
        # Can move only diagonally, so we can use y = mx + c
        # To solve the locations we have grad = +- 1
        values = np.arange(0, self.BOARD_SIZE).tolist()
        values.remove(self.x_coordinate)

        # Positive grad, Negative grad
        c_pos = -self.x_coordinate + self.y_coordinate
        c_neg = self.x_coordinate + self.y_coordinate

        pos_diagonal_moves = [(x, x + c_pos) for x in values if 0 <= x + c_pos < self.BOARD_SIZE]
        neg_diagonal_moves = [(x, -x + c_neg) for x in values if 0 <= -x + c_neg < self.BOARD_SIZE]
        self.possible_moves = pos_diagonal_moves + neg_diagonal_moves

        self.possible_moves = [x for x in self.possible_moves if x not in self.occupied_squares]
        return self.possible_moves

    def rook(self) -> list:
        # Rook can either move up or down or castle
        # if not self.moved:
        # self.possible_moves.append('Castle')

        for vertical_square in range(0, 8):
            vertical_move = (self.x_coordinate, vertical_square)
            if vertical_move == (self.x_coordinate, self.y_coordinate):
                continue
            self.possible_moves.append(vertical_move)

        for horizontal_square in range(0, 8):
            horizontal_move = (horizontal_square, self.y_coordinate)
            if horizontal_move == (self.x_coordinate, self.y_coordinate):
                continue
            self.possible_moves.append(horizontal_move)

        self.possible_moves = [x for x in self.possible_moves if x not in self.occupied_squares]
        return self.possible_moves

    def queen(self) -> list:

        values = np.arange(0, self.BOARD_SIZE).tolist()
        values.remove(self.x_coordinate)

        # Positive grad, Negative grad
        c_pos = -self.x_coordinate + self.y_coordinate
        c_neg = self.x_coordinate + self.y_coordinate

        pos_diagonal_moves = [(x, x + c_pos) for x in values if 0 <= x + c_pos < self.BOARD_SIZE]
        neg_diagonal_moves = [(x, -x + c_neg) for x in values if 0 <= -x + c_neg < self.BOARD_SIZE]
        self.possible_moves = pos_diagonal_moves + neg_diagonal_moves

        for vertical_square in range(0, 8):
            vertical_move = (self.x_coordinate, vertical_square)
            if vertical_move == (self.x_coordinate, self.y_coordinate):
                continue
            self.possible_moves.append(vertical_move)

        for horizontal_square in range(0, 8):
            horizontal_move = (horizontal_square, self.y_coordinate)
            if horizontal_move == (self.x_coordinate, self.y_coordinate):
                continue
            self.possible_moves.append(horizontal_move)

        self.possible_moves = [x for x in self.possible_moves if x not in self.occupied_squares]
        return self.possible_moves

    def king(self) -> list:

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue

                if self.x_coordinate + dx <= self.BOARD_SIZE-1 and self.y_coordinate <= self.BOARD_SIZE-1:
                    self.possible_moves.append((self.x_coordinate + dx, self.y_coordinate + dy))

        self.possible_moves = [x for x in self.possible_moves if x not in self.occupied_squares]
        return self.possible_moves



Game = Game()
Game.Player_Turn()
