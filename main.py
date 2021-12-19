import random
from tkinter import *
from tkinter.ttk import Combobox, Style
from PIL import Image
from PIL import ImageTk
from tkinter import font
from cell import Cell, Player
from functools import partial
from players import RandomPlayer, HumanPlayer, TicTacToePlayer, create_from_string

BACKGROUND_COLOR = "#B1DDC6"
FIELD_SIZE = 3

board = []
player_1 = RandomPlayer(Player.CROSS)
player_2 = RandomPlayer(Player.ZERO)
player_turn = random.choice([player_1, player_2])  # type:TicTacToePlayer
winner = Player.NOT_SET
turn_count = 0


class WinStatus:
    def __init__(self, is_win=False, win_row=0, win_column=0, win_diag=0):
        self.is_win = is_win
        self.win_row = win_row
        self.win_column = win_column
        self.win_diag = win_diag

    def __str__(self):
        return f'{self.is_win} row={self.win_row} column={self.win_column} diag={self.win_diag}'


def center_window(window: Tk, width=300, height=500):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def next_player_turn():
    if player_turn is player_1:
        return player_2
    else:
        return player_1


def drop_board():
    global winner, player_turn, turn_count
    set_players()
    player_turn = random.choice([player_1, player_2])
    winner = Player.NOT_SET
    turn_count = 0

    highlight_winner()
    highlight_next_turn_player()

    for row in board:
        for cell in row:
            cell.drop_state()

    ai_player_turn()


def highlight_next_turn_player():
    if winner is Player.NOT_SET:
        if player_turn.player is Player.CROSS:
            crossPlayer.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOn)
            zeroPlayer.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOff)
        elif player_turn.player is Player.ZERO:
            crossPlayer.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOff)
            zeroPlayer.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOn)
        else:
            crossPlayer.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOff)
            zeroPlayer.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOff)
    else:
        crossPlayer.itemconfig(crossPlayerImage, image=crossPhotoImageTurnOff)
        zeroPlayer.itemconfig(zeroPlayerImage, image=zeroPhotoImageTurnOff)


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


def ai_player_turn():
    global player_turn, winner, turn_count
    if player_turn.__class__ is HumanPlayer:
        return
    if winner is Player.NOT_SET:
        if player_turn.turn(cells_board=board, player_turn=player_turn.player):
            turn_count += 1
            ai_player_win_status = get_game_state_after_player_turn(player_turn)
            player_turn = next_player_turn()
            highlight_game_state(ai_player_win_status)
            highlight_next_turn_player()
            if not player_turn.player.__class__ is HumanPlayer:
                window.after(500, ai_player_turn)


def get_game_state_after_player_turn(turn_player: TicTacToePlayer) -> WinStatus:
    global winner
    if winner is Player.NOT_SET:
        win_status = get_player_win_status(turn_player.player)
        if win_status.is_win:
            winner = turn_player.player
        elif turn_count == FIELD_SIZE * FIELD_SIZE:
            winner = Player.NOBODY
        return win_status
    return WinStatus()


def highlight_game_state(win_status: WinStatus):
    highlight_win_on_board(win_status)
    highlight_winner()


def board_clicked(button: Cell):
    global player_turn, winner, turn_count
    if not (winner is Player.NOT_SET):
        return

    cell_is_clicked = player_turn.turn(button=button, player_turn=player_turn.player)
    if cell_is_clicked:
        turn_count += 1
        player_winn_status = get_game_state_after_player_turn(player_turn)
        highlight_game_state(player_winn_status)
        player_turn = next_player_turn()
        highlight_next_turn_player()

        window.after(500, ai_player_turn)


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
    if winner is Player.CROSS:
        winnerLabelCross.config(fg='red', text='Winner!')
        winnerLabelCross.pack(side='left')
        return
    if winner is Player.ZERO:
        winnerLabelCross.config(fg='red', text='Winner!')
        winnerLabelCross.pack(side='right')
        return
    if winner is Player.NOBODY:
        winnerLabelCross.config(fg='red', text='Draw!')
        winnerLabelCross.pack(side='top')
        return
    if winner is Player.NOT_SET:
        winnerLabelCross.config(fg=BACKGROUND_COLOR)
        return


def get_player_win_status(player: Player) -> WinStatus:
    for row in range(0, FIELD_SIZE):
        row_is_win = True
        for column in range(0, FIELD_SIZE):
            row_is_win = row_is_win and (board[row][column].state == player)
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

    return WinStatus()


def set_players(*args):
    global player_1, player_2, player_turn
    if player_turn is player_1:
        player_1 = create_from_string(selected_cross.get(), Player.CROSS)
        player_2 = create_from_string(selected_zero.get(), Player.ZERO)
        player_turn = player_1
    else:
        player_1 = create_from_string(selected_cross.get(), Player.CROSS)
        player_2 = create_from_string(selected_zero.get(), Player.ZERO)
        player_turn = player_2
    ai_player_turn()


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
    headerFrame = Frame(width=40, height=50, background=BACKGROUND_COLOR, padx=0, pady=0)
    headLabel = Label(headerFrame, width=200, text='Lets Play!', padx=0,
                      pady=10,
                      bg=BACKGROUND_COLOR, bd=0)
    headLabel.config(font=font.Font(family="Bradley Hand", size=40))
    headLabel.pack(side='top', pady=(0, 0))

    headerFrame.pack(side='top')

    # Winners
    winnersFrame = Frame(width=230, height=25, padx=0, pady=0, background=BACKGROUND_COLOR, )
    winnerLabelCross = Label(winnersFrame, height=25, text='Winner!', padx=0,
                             pady=20,
                             bg=BACKGROUND_COLOR, fg=BACKGROUND_COLOR, bd=0)
    winnerLabelCross.config(font=font.Font(family="Bradley Hand", size=25, weight='bold'))
    winnerLabelCross.pack(side='left')

    winnersFrame.pack(side='top')
    winnersFrame.pack_propagate(0)
    # Players
    playersTurnFrame = Frame(width=200, height=70, background=BACKGROUND_COLOR, padx=0, pady=0)

    zeroPhotoImageTurnOn = PhotoImage(file=r"images/zero_turn_on_50_50.png")
    zeroPhotoImageTurnOff = PhotoImage(file=r"images/zero_turn_off_50_50.png")

    crossPhotoImageTurnOn = PhotoImage(file=r"images/cross_turn_on_50_50.png")
    crossPhotoImageTurnOff = PhotoImage(file=r"images/cross_turn_off_50_50.png")

    crossPlayer = Canvas(playersTurnFrame, width=50, height=50, bg=BACKGROUND_COLOR, highlightthickness=0)
    crossPlayerImage = crossPlayer.create_image(25, 25, image=crossPhotoImageTurnOn, anchor="center")
    crossPlayer.pack(side='left')

    zeroPlayer = Canvas(playersTurnFrame, width=50, height=50, bg=BACKGROUND_COLOR, highlightthickness=0)
    zeroPlayerImage = zeroPlayer.create_image(25, 25, image=zeroPhotoImageTurnOn, anchor="center")
    zeroPlayer.pack(side='right')

    playersTurnFrame.pack(side='top')
    playersTurnFrame.pack_propagate(0)

    # choose players type
    choosePlayersFrame = Frame(width=200, height=40, background=BACKGROUND_COLOR, padx=0, pady=0)
    options_player_1 = ['Human', 'Random']
    selected_cross = StringVar(window, options_player_1[0])
    selected_cross.trace('w', set_players)
    choose_players_font = font.Font(family="Bradley Hand", size=20)

    crossPlayerMenu = OptionMenu(choosePlayersFrame, selected_cross, *options_player_1)
    crossPlayerMenu.config(font=choose_players_font, bg=BACKGROUND_COLOR, padx=0,
                           highlightthickness=0)
    menu_1 = window.nametowidget(crossPlayerMenu.menuname)
    menu_1.config(font=choose_players_font)
    crossPlayerMenu.pack(side='left')

    options_player_2 = ['Human', 'Random']
    selected_zero = StringVar(window, options_player_2[0])
    selected_zero.trace('w', set_players)
    zeroPlayerMenu = OptionMenu(choosePlayersFrame, selected_zero, *options_player_2)
    zeroPlayerMenu.config(font=choose_players_font, bg=BACKGROUND_COLOR, padx=0,
                          highlightthickness=0)
    menu_2 = window.nametowidget(zeroPlayerMenu.menuname)
    menu_2.config(font=choose_players_font)
    zeroPlayerMenu.pack(side='right')

    choosePlayersFrame.pack(side='top')
    choosePlayersFrame.pack_propagate(0)

    # board
    create_board()

    drop_board()

    reset_game_button = Button(text='New game', font=font.Font(family="Bradley Hand", size=40), padx=0, pady=0,
                               highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=drop_board)
    reset_game_button.pack(side='top', padx=0, pady=5)

    window.mainloop()
