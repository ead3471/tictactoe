from abc import ABC, abstractmethod
from cell import Player, Cell
import random


def prepare_board_from_cells(cells_board: list) -> list:
    result_list = [cell.state for row in cells_board for cell in row]
    return result_list


class TicTacToePlayer(ABC):

    def __init__(self, player: Player):
        self.player = player

    @abstractmethod
    def turn(self, player_turn: Player, cells_board=None, button: Cell = None) -> bool:
        pass


def create_from_string(player_name: str, player: Player) -> TicTacToePlayer:
    if player_name == 'Random':
        return RandomPlayer(player)
    if player_name == 'Human':
        return HumanPlayer(player)
    return 'Human'


class HumanPlayer(TicTacToePlayer):

    def __init__(self, player=Player.CROSS):
        self.player = player

    def __str__(self):
        return 'Human'

    def turn(self, player_turn: Player, button: Cell, cells_board=None) -> bool:
        if self.player is player_turn:
            return button.click(self.player)
        else:
            return False


class RandomPlayer(TicTacToePlayer):

    def __str__(self):
        return 'Random'

    def __init__(self, player: Player = Player.ZERO):
        self.player = player

    def turn(self, cells_board, player_turn: Player) -> bool:
        if self.player is not player_turn:
            return False

        not_set_cells = [
            cell for row in cells_board for cell in row if cell.state is Player.NOT_SET]
        if len(not_set_cells) > 0:
            select_cell = random.choice(not_set_cells)  # type:Cell
            return select_cell.click(player_turn=self.player)
        return False


class MinMaxPlayer(TicTacToePlayer):

    def __init__(self, player: Player = Player.ZERO):
        self.player = player

    def turn(self, player_turn: Player, cells_board=None, button: Cell = None) -> bool:
        pass


if __name__ == '__main__':
    player_1 = HumanPlayer(Player.CROSS)
    player_2 = HumanPlayer(Player.ZERO)
    print(player_1.player)
    print(player_2.player)
