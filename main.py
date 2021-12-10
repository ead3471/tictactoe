from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import font
from cell import Cell
from functools import partial
import array

# Press the green button in the gutter to run the script.
BACKGROUND_COLOR = "#B1DDC6"

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
is_cross_turn = True


def center_window(window: Tk, width=300, height=450):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


# board_array = array('i', [0, 0, 0][0, 0, 0][0, 0, 0])


def drop_board():
    for row in board:
        for cell in row:
            cell.drop_state()


def highlight_turn():
    if is_cross_turn:
        crossPlayerTurn.config(highlightthickness=1)
        zeroPlayerTurn.config(highlightthickness=0)
    else:
        zeroPlayerTurn.config(highlightthickness=1)
        crossPlayerTurn.config(highlightthickness=0)

def board_clicked(button: Cell):
    global is_cross_turn
    button.click(is_cross_turn)
    is_cross_turn = not is_cross_turn
    highlight_turn()


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

    img = Image.open("images/CROSS_50_50.png")
    img = img.resize((50, 50), Image.ADAPTIVE)
    crossPhotoImage = ImageTk.PhotoImage(img)
    crossPlayerTurn = Canvas(headerFrame, width=100, height=70, bg=BACKGROUND_COLOR, highlightthickness=0)
    crossImage = crossPlayerTurn.create_image(50, 25, image=crossPhotoImage, anchor="center")
    crossPlayerTurn.pack(side='left')

    zeroPhotoImage = PhotoImage(file=r"images/ZERO_50_50.png")
    zeroPlayerTurn = Canvas(headerFrame, width=100, height=70, bg=BACKGROUND_COLOR, highlightthickness=0)
    zeroImage = zeroPlayerTurn.create_image(50, 25, image=zeroPhotoImage, anchor="center")
    zeroPlayerTurn.pack(side='right')

    headerFrame.pack(side='top')

    highlight_turn()
    for row in range(0, 3):
        row_frame = Frame(width=200, height=100, background=BACKGROUND_COLOR)
        for column in range(0, 3):
            button = Cell(row_frame, cross_cell, zero_cell, empty_cell, name=f'{row}_{column}')
            button['command'] = partial(board_clicked, button)
            button.pack(side='left')
            board[row][column] = button
        row_frame.pack(side='top')

    reset_game_button = Button(text='New game', font=font.Font(family="Bradley Hand", size=40), padx=0, pady=0,
                               highlightthickness=0, command=drop_board)
    reset_game_button.pack(side='top', padx=0, pady=5)

    window.mainloop()
