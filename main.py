from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import font
from cell import Cell, CellState
from functools import partial

BACKGROUND_COLOR = "#B1DDC6"
FIELD_SIZE = 3

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
player_turn = CellState.CROSS  # type:CellState
winner = CellState.NOT_SET


class WinStatus:
    def __init__(self, is_win=False, win_row=0, win_column=0, win_diag=0):
        self.is_win = is_win
        self.win_row = win_row
        self.win_column = win_column
        self.win_diag = win_diag

    def __str__(self):
        return f'{self.is_win} row={self.win_row} column={self.win_column} diag={self.win_diag}'


def center_window(window: Tk, width=300, height=450):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def drop_board():
    for row in board:
        for cell in row:
            cell.drop_state()


def highlight_turn():
    if player_turn is CellState.CROSS:
        crossPlayerTurn.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOn)
        zeroPlayerTurn.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOff)
    else:
        crossPlayerTurn.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOff)
        zeroPlayerTurn.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOn)


def create_board():
    for row in range(0, FIELD_SIZE):
        row_frame = Frame(width=200, height=100, background=BACKGROUND_COLOR)
        for column in range(0, FIELD_SIZE):
            button = Cell(row_frame, cross_cell, zero_cell, empty_cell, name=f'{row}_{column}')
            button['command'] = partial(board_clicked, button)
            button.pack(side='left')
            board[row][column] = button
        row_frame.pack(side='top')


def board_clicked(button: Cell):
    global player_turn, winner

    if winner is CellState.NOT_SET:
        button.click(player_turn)
        if player_turn is CellState.CROSS:
            win_status = get_player_win_status(CellState.CROSS)
            if win_status.is_win:
                winner = CellState.CROSS
        else:
            win_status = get_player_win_status(CellState.ZERO)
            if win_status.is_win:
                winner = CellState.ZERO
        highlight_win(win_status)

        player_turn = player_turn.next_turn()
        highlight_turn()


def highlight_win(win_status: WinStatus):
    if not win_status.is_win:
        return


    if win_status.win_row > 0:
        for column in range(0, FIELD_SIZE):
            board[win_status.win_row - 1][column].highlight_as_win()
        return

    if win_status.win_column > 0:
        for row in range(0, FIELD_SIZE):
            board[row][win_status.win_column - 1].highlight_as_win()
        return

    if win_status.win_diag > 0:
        if win_status.win_diag == 1:
            for cell in range(0, FIELD_SIZE):
                board[cell][cell].highlight_as_win()
        else:
            for cell in range(0, FIELD_SIZE):
                board[FIELD_SIZE - cell][cell].highlight_as_win()


def get_player_win_status(player: CellState) -> WinStatus:
    for row in range(0, FIELD_SIZE):
        row_is_win = True
        for column in range(0, FIELD_SIZE):
            row_is_win = row_is_win and (board[row][column].state == player)
            if not row_is_win:
                break
        if row_is_win:
            return WinStatus(True, win_row=row + 1)

    for column in range(0, FIELD_SIZE):
        column_is_win = True
        for row in range(0, FIELD_SIZE):
            column_is_win = column_is_win and (board[row][column].state is player)
            if not column_is_win:
                break
        if column_is_win:
            return WinStatus(True, win_column=column + 1)

    left_diag_is_win = True
    right_diag_is_win = True
    for column in range(0, FIELD_SIZE):
        left_diag_is_win = left_diag_is_win and (board[column][column].state is player)
        right_diag_is_win = right_diag_is_win and (
                board[FIELD_SIZE - column - 1][column].state is player)
    if left_diag_is_win:
        return WinStatus(True, win_diag=1)
    if right_diag_is_win:
        return WinStatus(True, win_diag=2)

    return WinStatus()


if __name__ == '__main__':
    window = Tk()
    window.title("Tic Tac Toe")
    window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
    # window.resizable(False, False)

    center_window(window)

    empty_cell = ImageTk.PhotoImage(Image.open('images/cell_50_50.png').resize((50, 50), Image.ANTIALIAS))
    cross_cell = ImageTk.PhotoImage(Image.open('images/cell_cross_50_50.png').resize((50, 50), Image.ADAPTIVE))
    zero_cell = ImageTk.PhotoImage(Image.open('images/cell_zero_50_50.png').resize((50, 50), Image.ADAPTIVE))

    headerFrame = Frame(width=40, height=50, background=BACKGROUND_COLOR, padx=0, pady=5)
    headLabel = Label(headerFrame, width=200, text='Lets Play!', padx=0,
                      pady=0,
                      bg=BACKGROUND_COLOR, bd=0)
    headLabel.config(font=font.Font(family="Bradley Hand", size=40))
    headLabel.pack(side='top', pady=(10, 30))

    zeroPhotoImageTurnOn = PhotoImage(file=r"images/zero_turn_on_50_50.png")
    zeroPhotoImageTurnOff = PhotoImage(file=r"images/zero_turn_off_50_50.png")

    crossPhotoImageTurnOn = PhotoImage(file=r"images/cross_turn_on_50_50.png")
    crossPhotoImageTurnOff = PhotoImage(file=r"images/cross_turn_off_50_50.png")

    crossPlayerTurn = Canvas(headerFrame, width=100, height=50, bg=BACKGROUND_COLOR, highlightthickness=0)
    crossPlayerImage = crossPlayerTurn.create_image(50, 25, image=crossPhotoImageTurnOn, anchor="center")
    crossPlayerTurn.pack(side='left')

    zeroPlayerTurn = Canvas(headerFrame, width=100, height=50, bg=BACKGROUND_COLOR, highlightthickness=0)
    zeroPlayerImage = zeroPlayerTurn.create_image(50, 25, image=zeroPhotoImageTurnOn, anchor="center")
    zeroPlayerTurn.pack(side='right')

    headerFrame.pack(side='top')

    highlight_turn()

    create_board()

    reset_game_button = Button(text='New game', font=font.Font(family="Bradley Hand", size=40), padx=0, pady=0,
                               highlightthickness=0, command=drop_board)
    reset_game_button.pack(side='top', padx=0, pady=5)

    window.mainloop()
