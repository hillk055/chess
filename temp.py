piece = str(input('piece'))
        coordinates = np.where(self.board == piece)
        row, col = int(coordinates[0][0]), int(coordinates[1][0])
        turn = Pieces(row, col, )
        if piece not in self.moved.keys():
            moved = True
        if piece[1] == 'r':
            turn = Pieces(row, col, )
        if piece[1] == 'k':
            pass
        if piece[1] == 'b':
            pass
        if piece[1] == 'k':
            pass
        if piece[1] == 'q':
            pass
        if piece[1] == 'p':
            pass
        new_position = str(input('new_position'))
        new_row = int(new_position[0])
        new_col = int(new_position[1])
        print(new_row, new_col)
        self.board[row][col] = '_'
        self.board[new_row][new_col] = piece
        print(self.board)
