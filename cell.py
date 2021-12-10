from tkinter import Button


class Cell(Button):
    cross_turn = True
    instances = []

    @classmethod
    def drop_board(cls):
        Cell.cross_turn

    def __init__(self, parent, cross_img, zero_img, empty_img, x, y):
        self.clicked = False
        self.empty_img = empty_img
        self.cross_img = cross_img
        self.zero_img = zero_img
        self.x = x
        self.y = y
        Cell.instances.append(self)
        super().__init__(parent, padx=0, pady=0, image=empty_img, highlightthickness=0, command=lambda: self.click())

    def click(self):
        if self.clicked:
            return

        if Cell.cross_turn:
            self.config(image=self.cross_img)
        else:
            self.config(image=self.zero_img)

        self.clicked = True
        Cell.cross_turn = not Cell.cross_turn

    def drop_state(self):
        self.clicked = False
        self.config(image=self.empty_img)

    @classmethod
    def drop_all_cells(cls):
        for cell in Cell.instances:
            cell.drop_state()
