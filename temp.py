import numpy as np


class ChessGame:

    def __init__(self):
        self.board = [
            ['br1', 'bn1', 'bb1', 'bq', 'bk', 'bb2', 'bn2', 'br2'],
            ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
            ['wr1', 'wn1', 'wb1', 'wq', 'wk', 'wb2', 'wn2', 'wr2']

        ]
        self.moved = {
            'bp1': False, 'bp2': False, 'bp3': False, 'bp4': False,
            'bp5': False, 'bp6': False, 'bp7': False, 'bp8': False,
            'wp1': False, 'wp2': False, 'wp3': False, 'wp4': False,
            'wp5': False, 'wp6': False, 'wp7': False, 'wp8': False,
            'wk': False, 'wr1': False, 'br1': False, 'br2': False
        }
        self.board = np.array(self.board)
        self.counter = 0
        self.color_turn = 'w'
        self.king_in_check = False
        self.king_check_position = None

    def check(self, context, board, attacking_color, defending_color):

        all_color_moves = {}
        # Can maybe get rid of this depending on implementation if called directly
        # from update board this line is redundant
        for i, row in enumerate(board):
            for j, value in enumerate(row):
                if value == '_' or value[0] == attacking_color:
                    continue
                if value[1] == 'k':
                    king_position = (i, j)
                    print(king_position)
        for i1, row1 in enumerate(board):
            for j1, value1 in enumerate(row1):
                if value1 == '_' or value1[0] == defending_color:
                    continue
                find_piece = value1[1]
                has_moved = self.moved[value1] if value1 in self.moved.keys() else True
                moves = Pieces(i1, j1, has_moved, attacking_color, board, True)

                if find_piece == 'p':
                    all_moves = moves.pawn()
                    all_color_moves[value1] = all_moves
                elif find_piece == 'r':
                    all_moves = moves.rook()
                    all_color_moves[value1] = all_moves
                elif find_piece == 'n':
                    all_moves = moves.knight()
                    all_color_moves[value1] = all_moves
                elif find_piece == 'b':
                    all_moves = moves.bishop()
                    all_color_moves[value1] = all_moves
                elif find_piece == 'q':
                    all_moves = moves.queen()
                    all_color_moves[value1] = all_moves

        print(all_color_moves)


    def player_turn(self, row, col):

        if self.king_in_check:
            print('yes')
            self.must_move_king()
        self.color_turn = 'w' if self.counter % 2 == 0 else 'b'
        try:
            find_piece = self.board[row][col]
        except IndexError:
            return []
        if find_piece == '_':
            return []
        has_moved = self.moved[find_piece] if find_piece in self.moved.keys() else False
        color = find_piece[0]
        if color != self.color_turn:
            return []
        find_piece = find_piece[1]

        moves = Pieces(row, col, has_moved, color, self.board, False)

        if find_piece == 'p':

            return moves.pawn()
        elif find_piece == 'r':

            return moves.rook()
        elif find_piece == 'n':

            return moves.knight()
        elif find_piece == 'b':

            return moves.bishop()
        elif find_piece == 'q':

            return moves.queen()
        elif find_piece == 'k':

            return moves.king()


    def update_board(self, current_xy, new_xy):

        self.king_in_check = False
        piece_being_taken = None
        taking_piece = False
        self.color_turn = 'w' if self.counter % 2 == 0 else 'b'

        row, col = current_xy
        new_row, new_col = new_xy
        try:
            looking_for_piece = self.board[row][col]
        except IndexError:
            return []
        if looking_for_piece == '_':
            return []
        if looking_for_piece[0] != self.color_turn:
            return
        color = str(looking_for_piece[0])
        find_piece = looking_for_piece[1]

        has_moved = self.moved[find_piece] if find_piece in self.moved.keys() else False
        moves = Pieces(row, col, has_moved, color, self.board, False)


        if find_piece == 'p':

            moves_to_make= moves.pawn()
        elif find_piece == 'r':

            moves_to_make = moves.rook()
        elif find_piece == 'n':

            moves_to_make = moves.knight()
        elif find_piece == 'b':

            moves_to_make = moves.bishop()
        elif find_piece == 'q':

            moves_to_make = moves.queen()
        else:

            moves_to_make = moves.king()

        if new_xy in moves_to_make:
            if self.board[new_row][new_col][0] != self.color_turn and self.board[new_row][new_col] != '_':
                taking_piece = True
                piece_being_taken = self.board[new_row][new_col]
            piece_to_update = self.board[row][col]
            self.board[new_row][new_col] = self.board[row][col]
            self.board[row][col] = '_'
            if piece_to_update in self.moved.keys():
                self.moved[piece_to_update] = True

            self.check('Method1', self.board)
            self.counter += 1

            return looking_for_piece, new_xy, taking_piece, piece_being_taken, self.king_in_check, self.king_position

    def must_move_king(self):

        possible_moves_to_protect_king = []
        copy_board = np.copy(self.board)
        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                if value == '_':
                    continue
                piece = value
                row = i
                col = j
                has_moved = self.moved[piece] if piece in self.moved.keys() else False
                moves = Pieces(row, col, has_moved, piece[0], copy_board)
                moves_list = moves.pawn()
                for move in moves_list:
                    new_row = move[0]
                    new_col = move[1]
                    copy_board[new_row][new_col] = piece
                    copy_board[row][col] = '_'
                    print(copy_board)
                    copy_board = np.copy(self.board)
                    is_check = self.check('Method2', copy_board)
                    if not is_check:
                        possible_moves_to_protect_king.append((new_row, new_col))
        print(possible_moves_to_protect_king)



# noinspection PyUnboundLocalVariable
class Pieces:

    def __init__(self, row: int, column: int, moved, color: str, board, iteration) -> None:

        self.board = board
        self.BOARD_SIZE = 8
        self.color = color
        self.row = row
        self.column = column
        self.moved = moved
        self.possible_moves = []
        self.iteration = iteration

    def pawn(self) -> list:

        pass_moves = []
        if self.color == 'b':
            move_forward = 1
            first_move = 2
            if self.row + 1 < self.BOARD_SIZE and self.column + 1 < self.BOARD_SIZE:

                if (self.board[self.row + 1][self.column + 1] != '_' and
                        self.board[self.row + 1][self.column + 1][0] != self.color):

                    self.possible_moves.append((self.row + 1, self.column + 1))
                    pass_moves.append((self.row + 1, self.column + 1))

            elif self.row + 1 < self.BOARD_SIZE and self.column - 1 < self.BOARD_SIZE:
                if (self.board[self.row + 1][self.column - 1] != '_' and
                        self.board[self.row + 1][self.column - 1][0] != self.color):

                    self.possible_moves.append((self.row + 1, self.column - 1))
                    pass_moves.append((self.row + 1, self.column - 1))

            self.possible_moves.append((self.row + move_forward, self.column))

        elif self.color == 'w':
            move_forward = -1
            first_move = -2
            if self.row - 1 < self.BOARD_SIZE and self.column + 1 < self.BOARD_SIZE:

                if (self.board[self.row - 1][self.column + 1] != '_' and
                        self.board[self.row - 1][self.column + 1][0] != self.color):

                    self.possible_moves.append((self.row - 1, self.column + 1))
                    pass_moves.append((self.row - 1, self.column + 1))
            elif self.row - 1 < self.BOARD_SIZE and self.column - 1 < self.BOARD_SIZE:

                if (self.board[self.row - 1][self.column - 1] != '_' and
                        self.board[self.row - 1][self.column - 1][0] != self.color):

                    self.possible_moves.append((self.row - 1, self.column - 1))
                    pass_moves.append((self.row - 1, self.column - 1))

            self.possible_moves.append((self.row + move_forward, self.column))
        if not self.moved:
            self.possible_moves.append((self.row + first_move, self.column))

        remove_possible_squares = [(i, j) for i, j in self.possible_moves if self.board[i][j] != '_']

        for i in remove_possible_squares:
            if i in pass_moves:
                continue
            self.possible_moves.remove(i)
        return self.possible_moves

    def knight(self) -> list:

        # The knight cannot be blocked, so we do not need to check where it can move apart from the restrictions of the
        # board width.
        # return: List of possible moves for the knight given a starting point

        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:

                if (abs(dx) == 1 == abs(dy) == 1) or (abs(dx) == 2 == abs(dy) == 2):
                    continue
                if 0 <= self.row + dy < self.BOARD_SIZE and 0 <= self.column + dx < self.BOARD_SIZE:
                    if self.board[self.row + dy][self.column + dx][0] == self.color:
                        break
                    self.possible_moves.append((self.row + dy, self.column + dx))

        moves_not_allowed = [(i, j) for i, j in self.possible_moves if self.board[i][j][0] == self.color]
        for i in moves_not_allowed:
            self.possible_moves.remove(i)

        return self.possible_moves

    def bishop(self, board, row, column) -> list:
        
        # Can move only diagonally, so we can use y = mx + c
        # To solve the locations we have grad = +- 1
        values = np.arange(0, self.BOARD_SIZE)

        # Positive grad, Negative grad
        c_pos = -self.column + self.row
        c_neg = self.column + self.row

        pos_diagonal_moves = [(x + c_pos, x) for x in values if 0 <= x + c_pos < self.BOARD_SIZE]
        neg_diagonal_moves = [(-x + c_neg, x) for x in values if 0 <= -x + c_neg < self.BOARD_SIZE]

        index_of_current_position = pos_diagonal_moves.index((self.row, self.column))
        for move in pos_diagonal_moves[index_of_current_position + 1:]:
            rows = move[0]
            col = move[1]
            if self.board[rows][col] != '_':
                if self.board[rows][col][0] != self.color:
                    self.possible_moves.append(move)
                    break
                break
            self.possible_moves.append(move)
        for move in pos_diagonal_moves[:index_of_current_position][::-1]:
            rows = move[0]
            col = move[1]
            if self.board[rows][col] != '_':
                if self.board[rows][col][0] != self.color:
                    self.possible_moves.append(move)
                    break
                break
            self.possible_moves.append(move)

        # NEXT

        index_of_current_position = neg_diagonal_moves.index((self.row, self.column))
        for move in neg_diagonal_moves[index_of_current_position + 1:]:
            rows = move[0]
            col = move[1]
            if self.board[rows][col] != '_':
                if self.board[rows][col][0] != self.color:
                    self.possible_moves.append(move)
                    break
                break
            self.possible_moves.append(move)
        for move in neg_diagonal_moves[:index_of_current_position][::-1]:
            rows = move[0]
            col = move[1]
            if self.board[rows][col] != '_':
                if self.board[rows][col][0] != self.color:
                    self.possible_moves.append(move)
                    break
                break
            self.possible_moves.append(move)
        return self.possible_moves

    def rook(self) -> list:
        # Horizontal square
        for position in range(self.column-1, -1, -1):
            square = (self.row, position)
            if self.board[self.row][position] != '_':
                if self.board[self.row][position][0] != self.color:
                    self.possible_moves.append(square)
                break
            self.possible_moves.append(square)
        for position in range(self.column+1, self.BOARD_SIZE, 1):
            square = (self.row, position)
            if self.board[self.row][position] != '_':
                if self.board[self.row][position][0] != self.color:
                    self.possible_moves.append(square)
                break
            self.possible_moves.append(square)
        # Vertical square
        for position in range(self.row-1, -1, -1):
            square = (position, self.column)
            if self.board[position][self.column] != '_':
                if self.board[position][self.column][0] != self.color:
                    self.possible_moves.append(square)
                break
            self.possible_moves.append(square)
        for position in range(self.row+1, self.BOARD_SIZE, 1):
            square = (position, self.column)
            if self.board[position][self.column] != '_':
                if self.board[self.row][position][0] != self.color:
                    self.possible_moves.append(square)
                break
            self.possible_moves.append(square)
        return self.possible_moves

    def queen(self) -> list:

        moves_not_allowed = []
        squares1 = self.rook()
        squares2 = self.bishop()
        self.possible_moves = squares1 + squares2

        for move in self.possible_moves:
            row, col = move
            if self.board[row][col][0] == self.color:
                moves_not_allowed.append((row, col))

        try:
            self.possible_moves.remove(moves_not_allowed)
        except ValueError:
            pass
        return self.possible_moves

    def king(self) -> list:

        all_color_moves = []
        king_moves = [-1, 0, 1]
        for dx in king_moves:
            for dy in king_moves:
                if dx == dy == 0:
                    continue
                square = [(self.row+dy, self.column+dx)]

                if 0 <= square[0][0] <= self.BOARD_SIZE-1 and 0 <= square[0][1] <= self.BOARD_SIZE-1:
                    if self.board[square[0][0]][square[0][1]] == self.color:
                        break
                    self.possible_moves.append((self.row + dy, self.column + dx))
        moves_not_possible = []
        for move in self.possible_moves:
            row, col = move
            if self.board[row][col][0] == self.color:
                moves_not_possible.append((row, col))

        self.possible_moves = [x for x in self.possible_moves if x not in moves_not_possible]

        # Can maybe get rid of this depending on implementation if called directly
        # from update board this line is redundant
        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                if value == '_':
                    continue
                if value[1] == 'k' and value[0] != self.color:
                    self.king_position = (i, j)
                if value[0] == self.color:
                    find_piece = value[1]

                    if find_piece == 'p':
                        all_moves = self.pawn()

                    elif find_piece == 'r':
                        all_moves = self.rook()
                    elif find_piece == 'n':
                        all_moves = self.knight()
                    elif find_piece == 'b':
                        all_moves = self.bishop()

                    elif find_piece == 'q':
                        all_moves = self.queen()

                    all_color_moves.extend(all_moves)  # Extend the list with all possible moves
        for i in all_color_moves:
            if i in self.possible_moves:
                self.possible_moves.remove(i)
        return self.possible_moves
