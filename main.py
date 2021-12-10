from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import font
from cell import Cell
import array

# Press the green button in the gutter to run the script.
BACKGROUND_COLOR = "#B1DDC6"

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


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
    Cell.cross_turn = True
    Cell.drop_all_cells()


def board_clicked():
    print('here')


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


    boardFrameRow1 = Frame(width=200, height=100, background=BACKGROUND_COLOR)
    boardFrameRow1.pack(side='top')

    button_00 = Cell(boardFrameRow1, cross_cell, zero_cell, empty_cell, 0, 0)
    button_00.pack(side='left')
    board[0][0] = button_00

    button_01 = Cell(boardFrameRow1, cross_cell, zero_cell, empty_cell, 0, 1)
    button_01.pack(side='left')
    board[0][1] = button_01

    button_02 = Cell(boardFrameRow1, cross_cell, zero_cell, empty_cell, 0, 2)
    button_02.pack(side='left')
    board[0][2] = button_02

    boardFrameRow2 = Frame(width=200, height=100, background=BACKGROUND_COLOR)
    boardFrameRow2.pack(side='top')
    button_10 = Cell(boardFrameRow2, cross_cell, zero_cell, empty_cell, 1, 0)
    button_10.pack(side='left')
    button_11 = Cell(boardFrameRow2, cross_cell, zero_cell, empty_cell, 1, 1)
    button_11.pack(side='left')
    button_12 = Cell(boardFrameRow2, cross_cell, zero_cell, empty_cell, 1, 2)
    button_12.pack(side='left')

    boardFrameRow3 = Frame(width=200, height=100, background=BACKGROUND_COLOR)
    boardFrameRow3.pack(side='top')
    button_20 = Cell(boardFrameRow3, cross_cell, zero_cell, empty_cell, 2, 0)
    button_20.pack(side='left')
    button_21 = Cell(boardFrameRow3, cross_cell, zero_cell, empty_cell, 2, 1)
    button_21.pack(side='left')
    button_22 = Cell(boardFrameRow3, cross_cell, zero_cell, empty_cell, 2, 2)
    button_22.pack(side='left')

    reset_game_button = Button(text='New game', font=font.Font(family="Bradley Hand", size=40), padx=0, pady=0,
                               highlightthickness=0, command=drop_board)
    reset_game_button.pack(side='top', padx=0, pady=5)

    window.mainloop()
