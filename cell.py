from tkinter import Button
from enum import Enum


class Cell(Button):
    def __init__(self, parent, cross_img, zero_img, empty_img, name=''):
        self.state = CellState.NOT_SET
        self.empty_img = empty_img
        self.cross_img = cross_img
        self.zero_img = zero_img
        self.name = name
        super().__init__(parent, padx=0, pady=0, image=empty_img, highlightthickness=0)

    def highlight_as_win(self):
        self.config(highlightbackground="red")

    def click(self, player_turn):
        if player_turn is CellState.CROSS:
            self.set_cross()
        else:
            self.set_zero()

    def set_cross(self):
        if self.state is CellState.NOT_SET:
            self.config(image=self.cross_img)
            self.state = CellState.CROSS

    def set_zero(self):
        if self.state is CellState.NOT_SET:
            self.config(image=self.zero_img)
            self.state = CellState.ZERO

    def drop_state(self):
        self.config(image=self.empty_img, highlightbackground="white")
        self.state = CellState.NOT_SET

    @classmethod
    def drop_all_cells(cls):
        for cell in Cell.instances:
            cell.drop_state()


class CellState(Enum):
    NOT_SET = 1
    ZERO = 2
    CROSS = 3
    NOBODY = 4

    def next_turn(self):
        if self is CellState.ZERO:
            return CellState.CROSS
        else:
            return CellState.ZERO
