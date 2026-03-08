import tkinter


WHITE = 1
BLACK = 2
SYMBOLS = 'ABCDEFGH'


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE

def gameplay(board):
    while not (board.mat()):
        choice = True
        crds_st = input('Введите начальное расположение фигуры: ')
        y_s, x_s = int(crds_st[1]) - 1, SYMBOLS.index(crds_st[0])
        crds_en = input('Введите конечное расположение фигуры: ')
        y_e, x_e = int(crds_en[1]) - 1, SYMBOLS.index(crds_en[0])
        if board.color == BLACK:
            y_s, x_s, y_e, x_e = 7 - y_s, x_s, 7 - y_e, x_e
        while choice:
            if board.move_piece(y_s, x_s, y_e, x_e):
                print('Был успешно сделан ход с поля', crds_st, 'на поле', crds_en)
                board.move_piece(y_s, x_s, y_e, x_e)
                choice = False
            else:
                print('Ход с поля', crds_st, 'на поле', crds_en, 'невозможен!')
                crds_st = input('Введите начальное расположение фигуры: ')
                y_s, x_s = int(crds_st[1]) - 1, SYMBOLS.index(crds_st[0])
                crds_en = input('Введите конечное расположение фигуры: ')
                y_e, x_e = int(crds_en[1]) - 1, SYMBOLS.index(crds_en[0])
                if board.color == BLACK:
                    y_s, x_s, y_e, x_e = 7 - y_s, x_s, 7 - y_e, x_e
        board.print_board()


class Pawn:
    def __init__(self, color):
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'P'

    def get_color(self):
        return self.color

    def can_move(self, board, row1, col1, row, col):
        self.row = row1
        self.col = col1
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        direction = 1
        start_row = 1

        if row == 0 or row == 7:
            piece = input('Введите первую букву фигуры, которую хотите поставить: ')
            while piece not in ('B', 'N', 'Q', 'R'):
                piece = input('Введите первую букву фигуры, которую хотите поставить: ')
            board.move_and_promote_pawn(row1, col1, row, col, piece)
            board.color = opponent(board.color)
            return True

        c1 = row - self.row == 1
        c2 = abs(self.col - col) == 1
        if c1 and c2 and (not (board.field[row][col] is None)) and board.field[row][col].get_color() != self.color:
            return True
        # ход на 1 клетку

        if self.row + direction == row and self.col == col and board.field[row][col] is None:
            return True


        # ход на 2 клетки из начального положения
        c9 = board.field[row][col] is None
        if self.row == start_row and self.row + 2 * direction == row and c9:
            return True
        return False

    def can_see(self, board, row, col, row1, col1, step=1):
        c1 = row1 - row == 1 if step == 1 else row - row1 == 1
        c2 = abs(col - col1) == 1
        if c1 and c2:
            return True
        return False

def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class PieceColor():
    def __init__(self, color):
        self.color = color

    def opponent(self):
        if self.color == WHITE:
            return PieceColor(BLACK).color
        return PieceColor(WHITE).color

    def is_black(self):
        return self.color == BLACK

    def is_white(self):
        return self.color == WHITE

    def __eq__(self, other):
        return self.color == other.color


class Board:
    def __init__(self):
        self.l_r = True
        self.r_r = True
        self.move = True
        self.king_crds = []
        self.color = WHITE
        self.field = [
            [
                Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
            ],
            [
                Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
                Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
            ],
            8 * [None], 8 * [None], 8 * [None], 8 * [None],
            [
                Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
                Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
            ],
            [
                Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
            ]
        ]
        self.nums = [i for i in range(1, 9)]
        self.symbs = SYMBOLS

    def shah(self, color=False, vyv=False):
        if not (color):
            color = self.color
        res = False
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if isinstance(self.field[i][j], King):
                    if self.field[i][j].get_color() == color:
                        self.king_crds = [i, j]
                        king_x, king_y = i, j
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if not self.field[i][j] is None:
                    if self.field[i][j].can_see(self, i, j, king_x, king_y, step=-1) and self.field[i][j].get_color() != color:
                        res = True
        if res and not (vyv):
            print('Вам был поставлен шах!')
        return res

    def mat(self):
        if self.shah():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i == 0 and j == 0) and self.king_crds[0] + i >= 0 and self.king_crds[0] + i <= 7 and self.king_crds[1] + i >= 0 and self.king_crds[1] + i <= 7:
                        if self.field[self.king_crds[0]][self.king_crds[1]].can_move(self, self.king_crds[0], self.king_crds[1], self.king_crds[0] + i, self.king_crds[1] + j):
                            return False
            print('Вам был поставлен мат!')
            return True


    def castling0(self):
        c1 = isinstance(self.field[0][0], Rook) and self.color == WHITE
        c2 = isinstance(self.field[7][0], Rook) and self.color == BLACK
        c7 = isinstance(self.field[0][4], King) and self.color == WHITE
        c8 = isinstance(self.field[7][4], King) and self.color == BLACK
        if not (c1 or c2):
            return False
        if not (c7 or c8):
            return False
        if not self.l_r:
            return False
        if not self.move:
            return False
        for i in range(1, 4):
            con1 = not (self.field[0][i] is None) and self.color == WHITE
            con2 = not (self.field[7][i] is None) and self.color == BLACK
            if con1 or con2:
                return False
        if self.color == WHITE:
            self.field[0][2] = self.field[0][4]
            self.field[0][4] = None
            self.field[0][3] = self.field[0][0]
            self.field[0][0] = None
        else:
            self.field[7][2] = self.field[7][4]
            self.field[7][4] = None
            self.field[7][3] = self.field[7][0]
            self.field[7][0] = None
        self.color = opponent(self.color)
        return True

    def castling7(self):
        c3 = isinstance(self.field[0][7], Rook) and self.color == WHITE
        c4 = isinstance(self.field[7][7], Rook) and self.color == BLACK
        c7 = isinstance(self.field[0][4], King) and self.color == WHITE
        c8 = isinstance(self.field[7][4], King) and self.color == BLACK
        if not (c3 or c4):
            return False
        if not (c7 or c8):
            return False
        if not self.r_r:
            return False
        if not self.move:
            return False
        for i in range(6, 4, -1):
            con1 = not (self.field[0][i] is None) and self.color == WHITE
            con2 = not (self.field[7][i] is None) and self.color == BLACK
            if con1 or con2:
                return False
        if self.color == WHITE:
            self.field[0][6] = self.field[0][4]
            self.field[0][4] = None
            self.field[0][5] = self.field[0][7]
            self.field[0][7] = None
        else:
            self.field[7][6] = self.field[7][4]
            self.field[7][4] = None
            self.field[7][5] = self.field[7][7]
            self.field[7][7] = None
        self.color = opponent(self.color)
        return True

    def print_board(self):  # Распечатать доску в текстовом виде (см. скриншот)
        master = tkinter.Tk()
        canvas = tkinter.Canvas(master, bg='#bf8d47', height=900, width=900)
        for j in range(2):
            for i in range(1, 9):
                if j == 0:
                    canvas.create_line((i * 100, 0), (i * 100, 900), fill='black')
                else:
                    canvas.create_line((0, i * 100), (900, i * 100), fill='black')
        self.field = self.field[::-1]
        self.nums = self.nums[::-1]
        for i in range(len(self.field) + 1):
            for j in range(len(self.field[0]) + 1):
                if i == len(self.field):
                    if j != 0:
                        print(j + 50, i + 50)
                        canvas.create_text(j * 100 + 50, i * 100 + 50, text=str(self.symbs[j - 1]), fill="black", font=('Arial bold', 28))
                else:
                    if i <= 7 and j <= 8:
                        if not self.field[i][j - 1] is None:
                            if self.field[i][j - 1].get_color() == WHITE:
                                color = 'white'
                                arccolor = 'black'
                            else:
                                color = 'black'
                                arccolor = 'white'
                        if j == 0:
                            canvas.create_text(50, i * 100 + 50, text=str(self.nums[i]), fill="black", font=('Arial bold', 28))
                        else:
                            if isinstance(board.field[i][j - 1], Pawn):
                                canvas.create_oval(j * 100 + 41, i * 100 + 10, j * 100 + 59, i * 100 + 28, fill=color, outline='black')
                                canvas.create_oval(j * 100 + 35, i * 100 + 23, j * 100 + 65, i * 100 + 53, fill=color, outline='black')
                                canvas.create_arc(j * 100 + 20, i * 100 + 49, j * 100 + 80, i * 100 + 121, start=0, extent=180,
                                                  fill=color, outline='black')


                            if isinstance(board.field[i][j - 1], Bishop):
                                canvas.create_oval(j * 100 + 45, i * 100 + 10, j * 100 + 55, i * 100 + 20, fill=color, outline=arccolor)
                                canvas.create_oval(j * 100 + 33, i * 100 + 20, j * 100 + 67, i * 100 + 54, fill=color, outline=arccolor)
                                canvas.create_oval(j * 100 + 38, i * 100 + 54, j * 100 + 62, i * 100 + 62, fill=color, outline=arccolor)
                                canvas.create_oval(j * 100 + 36, i * 100 + 62, j * 100 + 64, i * 100 + 70, fill=color, outline=arccolor)
                                canvas.create_polygon(j * 100 + 10, i * 100 + 90, j * 100 + 10, i * 100 + 85,
                                                      j * 100 + 45, i * 100 + 70, j * 100 + 55, i * 100 + 70,
                                                      j * 100 + 90, i * 100 + 85, j * 100 + 90, i * 100 + 90,
                                                      j * 100 + 48, i * 100 + 80, j * 100 + 52, i * 100 + 80,
                                                      fill=color, outline=arccolor)
                                canvas.create_line(j * 100 + 41, i * 100 + 37, j * 100 + 59, i * 100 + 37, fill=arccolor, width=1.5)
                                canvas.create_line(j * 100 + 50, i * 100 + 28, j * 100 + 50, i * 100 + 46, fill=arccolor, width=1.5)


                            if isinstance(board.field[i][j - 1], Knight):
                                canvas.create_arc(j * 100 + 50, i * 100 + 20, j * 100 + 90, i * 100 + 105, start=325, extent=220, fill=color, outline='black')
                                canvas.create_polygon(j * 100 + 86, i * 100 + 90, j * 100 + 65, i * 100 + 20,
                                                      j * 100 + 50, i * 100 + 10, j * 100 + 45, i * 100 + 20,
                                                      j * 100 + 43, i * 100 + 20, j * 100 + 29, i * 100 + 10,
                                                      j * 100 + 30, i * 100 + 20, j * 100 + 10, i * 100 + 55,
                                                      j * 100 + 20, i * 100 + 63, j * 100 + 50, i * 100 + 50,
                                                      j * 100 + 50, i * 100 + 54, j * 100 + 30, i * 100 + 90,
                                                      fill=color, outline='black')
                                canvas.create_oval(j * 100 + 18, i * 100 + 50, j * 100 + 21, i * 100 + 53, fill=arccolor)
                                canvas.create_oval(j * 100 + 33, i * 100 + 27, j * 100 + 36, i * 100 + 35, fill=arccolor)


                            if isinstance(board.field[i][j - 1], Rook):
                                canvas.create_rectangle(j * 100 + 10, i * 100 + 84, j * 100 + 90, i * 100 + 90, fill=color, outline='black')
                                canvas.create_rectangle(j * 100 + 20, i * 100 + 77, j * 100 + 80, i * 100 + 84, fill=color, outline='black')
                                canvas.create_rectangle(j * 100 + 25, i * 100 + 33, j * 100 + 75, i * 100 + 77, fill=color, outline='black')
                                canvas.create_polygon(j * 100 + 25, i * 100 + 28, j * 100 + 10, i * 100 + 18,
                                                      j * 100 + 10, i * 100 + 10, j * 100 + 23, i * 100 + 10,
                                                      j * 100 + 23, i * 100 + 18, j * 100 + 40, i * 100 + 18,
                                                      j * 100 + 40, i * 100 + 10, j * 100 + 60, i * 100 + 10,
                                                      j * 100 + 60, i * 100 + 18, j * 100 + 77, i * 100 + 18,
                                                      j * 100 + 77, i * 100 + 10, j * 100 + 90, i * 100 + 10,
                                                      j * 100 + 90, i * 100 + 18, j * 100 + 75, i * 100 + 28,
                                                      j * 100 + 75, i * 100 + 33, j * 100 + 25, i * 100 + 33,
                                                      fill=color, outline='black')
                                canvas.create_line(j * 100 + 10, i * 100 + 84, j * 100 + 90, i * 100 + 84, fill=arccolor)
                                canvas.create_line(j * 100 + 20, i * 100 + 77, j * 100 + 80, i * 100 + 77, fill=arccolor)
                                canvas.create_line(j * 100 + 25, i * 100 + 30.5, j * 100 + 75, i * 100 + 30.5, fill=arccolor)
                                canvas.create_line(j * 100 + 25, i * 100 + 28, j * 100 + 75, i * 100 + 28, fill=arccolor)
                                canvas.create_line(j * 100 + 20, i * 100 + 25, j * 100 + 80, i * 100 + 25, fill=arccolor)

                            #!!
                            if isinstance(board.field[i][j - 1], Queen):
                                canvas.create_oval(j * 100 + 18, i * 100 + 78, j * 100 + 82, i * 100 + 90, fill=color, outline=arccolor)
                                canvas.create_oval(j * 100 + 21, i * 100 + 70, j * 100 + 79, i * 100 + 82, fill=color, outline=arccolor)
                                canvas.create_oval(j * 100 + 17, i * 100 + 62, j * 100 + 83, i * 100 + 74, fill=color, outline=arccolor)
                                canvas.create_oval(j * 100 + 10, i * 100 + 16, j * 100 + 16, i * 100 + 22, fill=color,
                                                   outline='black')
                                canvas.create_polygon(j * 100 + 13.5, i * 100 + 22, j * 100 + 18, i * 100 + 65,
                                                      j * 100 + 31, i * 100 + 64, fill=color, outline='black')

                                canvas.create_oval(j * 100 + 27, i * 100 + 13, j * 100 + 33, i * 100 + 19, fill=color,
                                                   outline='black')
                                canvas.create_polygon(j * 100 + 30.5, i * 100 + 19, j * 100 + 31, i * 100 + 64,
                                                      j * 100 + 44, i * 100 + 63, fill=color, outline='black')

                                canvas.create_oval(j * 100 + 47, i * 100 + 11, j * 100 + 53, i * 100 + 17, fill=color,
                                                   outline='black')
                                canvas.create_polygon(j * 100 + 50, i * 100 + 17, j * 100 + 44, i * 100 + 62,
                                                      j * 100 + 56, i * 100 + 62, fill=color, outline='black')

                                canvas.create_oval(j * 100 + 67, i * 100 + 13, j * 100 + 73, i * 100 + 19, fill=color,
                                                   outline='black')
                                canvas.create_polygon(j * 100 + 69.5, i * 100 + 19, j * 100 + 56, i * 100 + 63,
                                                      j * 100 + 69, i * 100 + 64, fill=color, outline='black')

                                canvas.create_oval(j * 100 + 84, i * 100 + 16, j * 100 + 90, i * 100 + 22, fill=color,
                                                   outline='black')
                                canvas.create_polygon(j * 100 + 86.5, i * 100 + 22, j * 100 + 69, i * 100 + 64,
                                                      j * 100 + 82, i * 100 + 65, fill=color, outline='black')


                            if isinstance(board.field[i][j - 1], King):
                                canvas.create_oval(j * 100 + 10, i * 100 + 39, j * 100 + 52, i * 100 + 76, fill=color,
                                                   outline=arccolor)

                                canvas.create_oval(j * 100 + 48, i * 100 + 39, j * 100 + 90, i * 100 + 76, fill=color,
                                                   outline=arccolor)

                                canvas.create_oval(j * 100 + 22, i * 100 + 68, j * 100 + 78, i * 100 + 84, fill=color,
                                                   outline=arccolor)
                                canvas.create_oval(j * 100 + 22, i * 100 + 73.5, j * 100 + 78, i * 100 + 87, fill=color,
                                                   outline=arccolor)
                                canvas.create_oval(j * 100 + 22, i * 100 + 79, j * 100 + 78, i * 100 + 90, fill=color,
                                                   outline=arccolor)



                                canvas.create_oval(j * 100 + 42, i * 100 + 23, j * 100 + 58, i * 100 + 47.5, fill=color,
                                                   outline=arccolor)
                                canvas.create_line(j * 100 + 50, i * 100 + 10, j * 100 + 50, i * 100 + 23, fill='black', width=1.8)
                                canvas.create_line(j * 100 + 44, i * 100 + 13.5, j * 100 + 56, i * 100 + 13.5, fill='black', width=1.8)

        canvas.pack()
        master.mainloop()

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        color = self.field[row][col].get_color()
        if self.field[row][col].char() != 'P':
            return False
        if row != 1 and row != 6:
            return False
        if abs(col - col1) >= 2:
            return False
        if col == col1:
            if not (self.field[row1][col1] is None):
                return False
            else:
                if char == 'R':
                    self.field[row1][col1] = Rook(color)
                if char == 'B':
                    self.field[row1][col1] = Bishop(color)
                if char == 'N':
                    self.field[row1][col1] = Knight(color)
                if char == 'Q':
                    self.field[row1][col1] = Queen(color)
                self.field[row][col] = None
                for i in self.field:
                    print(i)
                return True
        if abs(col - col1) == 1:
            if self.field[row1][col1] is None:
                return False
            if self.field[row1][col1].get_color() == color or self.field[row1][col1].char() == 'K':
                return False
            if char == 'R':
                self.field[row1][col1] = Rook(color)
            if char == 'B':
                self.field[row1][col1] = Bishop(color)
            if char == 'N':
                self.field[row1][col1] = Knight(color)
            if char == 'Q':
                self.field[row1][col1] = Queen(color)
            self.field[row][col] = None
            return True

    def get_piece(self, row, col):
        return self.field[row][col]

    def current_player_color(self):
        return self.color

    def get_color(self, row, col):
        el = self.field[row][col]
        color = el.get_color()
        return color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        piece2 = self.field[row1][col1]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if isinstance(self.field[row][col], King) and abs(col - col1) > 1:
            if col1 == 6:
                if self.castling7():
                    self.castling7()
            if col1 == 2:
                if self.castling0():
                    self.castling0()
            return True
        if isinstance(self.field[row][col], Pawn) and (row1 == 0 or row1 == 7):
            piece.can_move(self, row, col, row1, col1)
            return True
        if not piece.can_move(self, row, col, row1, col1):
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if self.shah(vyv=True):
            self.field[row][col] = piece  # Поставить обратно.
            self.field[row1][col1] = piece2  # Поставить обратно.
            print('Ход невозможен, так как поставлен шах! Защищайтесь!')
            return False
        if isinstance(self.field[row1][col1], Rook):
            if col == 0:
                self.l_r = False
            if col == 7:
                self.r_r = False
        if isinstance(self.field[row1][col1], King):
            self.move = False
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
        return True

    def __str__(self):
        return self.print_board()


class Rook:
    def __init__(self, color):
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'R'

    def get_color(self):
        return self.color

    def can_move(self, board, row1, col1, row, col):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        self.row = row1
        self.col = col1
        c9 = board.field[row][col] is None
        if self.row != row and self.col != col and c9:
            return False
        if self.row == row and self.col == col:
            return False
        if self.row == row:
            for i in range(min([self.col, col]) + 1, max([self.col, col])):
                if not board.field[row][i] is None:
                    return False
        else:
            for i in range(min([self.row, row]) + 1, max([self.row, row])):
                if not board.field[i][col] is None:
                    return False
        c9 = not board.field[row][col] is None
        if c9:
            return False
        return True

    def can_see(self, board, row, col, row1, col1, step=False):
        c1 = row == row1
        c2 = col == col1
        if c1 or c2:
            if c1:
                for i in range(col + 1, col1):
                    if not board.field[row][i] is None:
                        return False
            if c2:
                for i in range(row + 1, row1):
                    if not board.field[i][col] is None:
                        return False
            return True
        return False


class King:
    def __init__(self, color):
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'K'

    def get_color(self):
        return self.color

    def can_see(self, board, row, col, row1, col1, step=False):
        c1 = abs(row - row1) <= 1
        c2 = abs(col - col1) <= 1
        if c1 and c2:
            return True
        return False

    def can_move(self, board, row1, col1, row, col):
        self.row = row1
        self.col = col1
        c1 = (abs(self.row - row) <= 1 and abs(self.col - col) <= 1)
        c2 = (abs(self.row - row) == 0 and abs(self.col - col) == 0)
        c9 = board.field[row][col] is None
        c3 = ((not (board.field[row][col] is None)) and board.field[row][col].get_color() != board.field[self.row][self.col].get_color())
        if (c1 and not (c2) and c9 and not (board.shah())) or (c1 and not(c2) and c3):
            return True
        return False


class Queen:
    def __init__(self, color):
        self.symbols = []
        self.color = color
        self.k = set()
        self.count = set()

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def char(self):
        return 'Q'

    def get_color(self):
        return self.color

    def can_move(self, board, row1, col1, row, col):
        self.row = row1
        self.col = col1
        c1 = abs(self.row - row) == abs(self.col - col)
        c2 = row <= 7 and row >= 0
        c3 = col <= 7 and col >= 0
        c4 = not (self.row == row and self.col == col)
        c5 = self.row == row
        c6 = self.col == col
        if (c2 and c3) and ((c1 and c4) or (c4 and (c5 or c6))):
            if (not (board.field[row][col] is None)) and self.color == board.get_color(row, col):
                return False
            if c1:
                if row - self.row == col - self.col:
                    if self.row - row < 0:
                        step = 1
                    else:
                        step = -1
                    for row1 in range(self.row + step, row + step, step):
                        col1 = self.col - self.row + row1
                        for j in self.symbols:
                            c1 = min([self.row, row, j[0]]) == j[0]
                            c2 = max([self.row, row, j[0]]) == j[0]
                            if (j[0] - self.row == j[1] - self.col and (not (c1 or c2))):
                                return False
                        if (not (board.field[row1][col1] is None)):
                            if self.color == board.get_color(row1, col1):
                                return False
                            else:
                                self.symbols.append([row1, col1])
                if self.col + self.row == col + row:
                    if self.row - row < 0:
                        step = 1
                    else:
                        step = -1
                    for row1 in range(self.row + step, row + step, step):
                        col1 = self.col + self.row - row1
                        for j in self.symbols:
                            c3 = min([self.row, row, j[0]]) == j[0]
                            c4 = max([self.row, row, j[0]]) == j[0]
                            if j[0] + j[1] == self.row + self.col and (not (c3 or c4)):
                                return False
                        if (not (board.field[row1][col1] is None)):
                            if self.color == board.get_color(row1, col1):
                                return False
                            else:
                                self.symbols.append([row1, col1])
            if c5:
                if self.col - col < 0:
                    step = 1
                else:
                    step = -1
                for i in range(self.col + step, col + step, step):
                    for j in range(1, 8):
                        if i - j * step >= 0 and i - j * step < 8:
                            c5 = min([self.col, col, i - j * step]) == i - j * step
                            c6 = max([self.col, col, i - j * step]) == i - j * step
                            if [self.row, i - j * step] in self.symbols and (not (c5 or c6)):
                                return False
                    if (not (board.field[self.row][i] is None)):
                        if self.color == board.get_piece(self.row, i).get_color():
                            return False
                        else:
                            self.symbols.append([self.row, i])

            if c6:
                if self.row - row < 0:
                    step = 1
                else:
                    step = -1
                for i in range(self.row + step, row + step, step):
                    for j in range(self.row + step, row + step, step):
                        if j != self.row:
                            c7 = min([self.row, row, j]) == j
                            c8 = max([self.row, row, j]) == j
                            if [j, self.col] in self.symbols and (not (c7 or c8)):
                                return False
                    if (not (board.field[i][self.col] is None)):
                        if self.color == board.get_piece(i, self.col).get_color():
                            return False
                        else:
                            self.symbols.append([i, self.col])
            return True
        return False

    def can_see(self, board, row, col, row1, col1, step=False):
        c1 = row == row1
        c2 = col == col1
        c3 = col + row == col1 + row1
        c4 = col1 - col == row1 - row
        if c1 or c2 or c3 or c4:
            if c1:
                for i in range(min([col, col1]) + 1, max([col, col1])):
                    if not board.field[row][i] is None:
                        return False
            if c2:
                for i in range(min([row, row1]) + 1, min([row, row1])):
                    if not board.field[i][col] is None:
                        return False
            if c3:
                for count in range(1, abs(col - col1)):
                    if row - row1 < 0:
                        count2 = count
                    if row - row1 > 0:
                        count2 = -count
                    if col - col1 > 0:
                        count = -count
                    if not board.field[row + count2][col + count] is None:
                        return False
            if c4:
                for count in range(1, abs(col - col1)):
                    if row1 - row < 0:
                        count = -count
                    if not board.field[row + count][col + count] is None:
                        return False
            return True
        return False


class Knight:
    def __init__(self, color):
        self.color = color

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def char(self):
        return 'N'

    def get_color(self):
        return self.color

    def can_move(self, board, row1, col1, row, col):
        self.row = row1
        self.col = col1
        c1 = (abs(self.row - row) == 1 and abs(self.col - col) == 2)
        c2 = (abs(self.row - row) == 2 and abs(self.col - col) == 1)
        c3 = row <= 7 and row >= 0
        c4 = col <= 7 and col >= 0
        c9 = board.field[row][col] is None
        c8 = not board.field[row][col] is None and board.field[row][col].get_color() != self.color
        if ((c1 or c2) and c3 and c4) and (c9 or c8):
            return True
        return False

    def can_see(self, board, row, col, row1, col1, step=False):
        c1 = (abs(row1 - row) == 1 and abs(col1 - col) == 2)
        c2 = (abs(row1 - row) == 2 and abs(col1 - col) == 1)
        if c1 or c2:
            return True
        return False


class Bishop:
    def __init__(self, color):
        self.color = color

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def char(self):
        return 'B'

    def get_color(self):
        return self.color

    def can_move(self, board, row1, col1, row, col):
        self.row = row1
        self.col = col1
        for i in range(1, abs(self.row - row)):
            if not board.field[self.row + i][self.col + i] is None:
                return False
        c1 = abs(self.row - row) == abs(self.col - col)
        c2 = row <= 7 and row >= 0
        c3 = col <= 7 and col >= 0
        c4 = self.row != row and self.col != col
        c9 = board.field[row][col] is None
        if c1 and c2 and c3 and c4 and c9:
            return True
        return False

    def can_see(self, board, row, col, row1, col1, step=False):
        c3 = col + row == col1 + row1
        c4 = col1 - col == row1 - row
        if c3 or c4:
            if c3:
                for count in range(1, abs(col - col1)):
                    if row - row1 < 0:
                        count2 = count
                    if row - row1 > 0:
                        count2 = -count
                    if col - col1 > 0:
                        count = -count
                    if not board.field[row + count2][col + count] is None:
                        return False
            if c4:
                for count in range(1, abs(col - col1)):
                    if row1 - row < 0:
                        count = -count
                    if not board.field[row + count][col + count] is None:
                        return False
            return True
        return False

board = Board()
gameplay(board)