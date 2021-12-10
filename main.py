from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import font
from cell import Cell, CellState
from functools import partial

BACKGROUND_COLOR = "#B1DDC6"
FIELD_SIZE = 3

board = []
player_turn = CellState.CROSS  # type:CellState
winner = CellState.NOT_SET
turn_count = 0


class WinStatus:
    def __init__(self, is_win=False, win_row=0, win_column=0, win_diag=0, not_check_cells_count=0):
        self.is_win = is_win
        self.win_row = win_row
        self.win_column = win_column
        self.win_diag = win_diag
        self.not_check_cells_count = not_check_cells_count

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
    global winner
    winner = CellState.NOT_SET
    highlight_winner()
    winnerLabelCross.config(fg=BACKGROUND_COLOR)

    for row in board:
        for cell in row:
            cell.drop_state()


def highlight_next_turn_player():
    if player_turn is CellState.CROSS:
        crossPlayer.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOn)
        zeroPlayer.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOff)
    else:
        crossPlayer.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOff)
        zeroPlayer.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOn)


def create_board():
    for row in range(0, FIELD_SIZE):
        row_frame = Frame(width=200, height=100, background=BACKGROUND_COLOR)
        board.append([])
        for column in range(0, FIELD_SIZE):
            button = Cell(row_frame, cross_cell, zero_cell, empty_cell, name=f'{row}_{column}')
            button['command'] = partial(board_clicked, button)
            button.pack(side='left')
            board[row].append(button)
        row_frame.pack(side='top')


def board_clicked(button: Cell):
    global player_turn, winner

    if winner is CellState.NOT_SET:
        cell_is_clicked = button.click(player_turn)
        if cell_is_clicked:
            win_status = get_player_win_status(player_turn)
            if win_status.is_win:
                winner = player_turn
                highlight_win_on_board(win_status)
                highlight_winner()
            elif win_status.not_check_cells_count == 0:
                winner = CellState.NOBODY
                highlight_winner()

            player_turn = player_turn.next_turn()
            highlight_next_turn_player()


def highlight_win_on_board(win_status: WinStatus):
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
                board[FIELD_SIZE - cell - 1][cell].highlight_as_win()


def highlight_winner():
    if winner is CellState.CROSS:
        winnerLabelCross.config(fg='red', text='Winner!')
        winnerLabelCross.pack(side='left')
        return
    if winner is CellState.ZERO:
        winnerLabelCross.config(fg='red', text='Winner!')
        winnerLabelCross.pack(side='right')
        return
    if winner is CellState.NOBODY:
        winnerLabelCross.config(fg='red', text='Draw!')
        winnerLabelCross.pack(side='top')
        return


def get_player_win_status(player: CellState) -> WinStatus:
    not_check_cells_count = 0
    for row in range(0, FIELD_SIZE):
        row_is_win = True
        for column in range(0, FIELD_SIZE):
            row_is_win = row_is_win and (board[row][column].state == player)
            if board[row][column].state is CellState.NOT_SET:
                not_check_cells_count += 1
        if row_is_win:
            return WinStatus(True, win_row=row + 1)

    for column in range(0, FIELD_SIZE):
        column_is_win = True
        for row in range(0, FIELD_SIZE):
            column_is_win = column_is_win and (board[row][column].state is player)
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

    return WinStatus(not_check_cells_count=not_check_cells_count)


if __name__ == '__main__':
    window = Tk()
    window.title("Tic Tac Toe")
    window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
    # window.resizable(False, False)

    center_window(window)

    empty_cell = ImageTk.PhotoImage(Image.open('images/cell_50_50.png').resize((50, 50), Image.ANTIALIAS))
    cross_cell = ImageTk.PhotoImage(Image.open('images/cell_cross_50_50.png').resize((50, 50), Image.ADAPTIVE))
    zero_cell = ImageTk.PhotoImage(Image.open('images/cell_zero_50_50.png').resize((50, 50), Image.ADAPTIVE))

    # Header
    headerFrame = Frame(width=40, height=50, background=BACKGROUND_COLOR, padx=0, pady=5)
    headLabel = Label(headerFrame, width=200, text='Lets Play!', padx=0,
                      pady=0,
                      bg=BACKGROUND_COLOR, bd=0)
    headLabel.config(font=font.Font(family="Bradley Hand", size=40))
    headLabel.pack(side='top', pady=(0, 0))
    headerFrame.pack(side='top')

    # Winners
    winnersFrame = Frame(width=230, height=25, padx=0, pady=0, background=BACKGROUND_COLOR, )
    winnerLabelCross = Label(winnersFrame, height=25, text='Winner!', padx=0,
                             pady=0,
                             bg=BACKGROUND_COLOR, fg=BACKGROUND_COLOR, bd=0)
    winnerLabelCross.config(font=font.Font(family="Bradley Hand", size=25, weight='bold'))
    winnerLabelCross.pack(side='left')

    # winnerLabelZero = Label(winnersFrame, height=25, text='WInner!', padx=0,
    #                         pady=0,
    #                         bg=BACKGROUND_COLOR, fg=BACKGROUND_COLOR, bd=0)
    # winnerLabelZero.config(font=font.Font(family="Bradley Hand", size=20))
    # winnerLabelZero.pack(side='right')

    winnersFrame.pack(side='top')
    winnersFrame.pack_propagate(0)
    # Players
    playersFrame = Frame(width=200, height=70, background=BACKGROUND_COLOR, padx=0, pady=0)

    zeroPhotoImageTurnOn = PhotoImage(file=r"images/zero_turn_on_50_50.png")
    zeroPhotoImageTurnOff = PhotoImage(file=r"images/zero_turn_off_50_50.png")

    crossPhotoImageTurnOn = PhotoImage(file=r"images/cross_turn_on_50_50.png")
    crossPhotoImageTurnOff = PhotoImage(file=r"images/cross_turn_off_50_50.png")

    crossPlayer = Canvas(playersFrame, width=50, height=50, bg=BACKGROUND_COLOR, highlightthickness=0)
    crossPlayerImage = crossPlayer.create_image(25, 25, image=crossPhotoImageTurnOn, anchor="center")
    crossPlayer.pack(side='left')

    zeroPlayer = Canvas(playersFrame, width=50, height=50, bg=BACKGROUND_COLOR, highlightthickness=0)
    zeroPlayerImage = zeroPlayer.create_image(25, 25, image=zeroPhotoImageTurnOn, anchor="center")
    zeroPlayer.pack(side='right')

    playersFrame.pack(side='top')
    playersFrame.pack_propagate(0)

    highlight_next_turn_player()

    # board
    create_board()

    reset_game_button = Button(text='New game', font=font.Font(family="Bradley Hand", size=40), padx=0, pady=0,
                               highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=drop_board)
    reset_game_button.pack(side='top', padx=0, pady=5)

    window.mainloop()
