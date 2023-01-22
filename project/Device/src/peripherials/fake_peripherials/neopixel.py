from .my_board import board


class NeoPixel:
    def __init__(self, board: board, number_of_diodes: int, brightness: float, auto_write: bool) -> None:
        self.board = board
        self.number_of_diodes = number_of_diodes
        self.brightness = brightness
        self.auto_write = auto_write
        self.diodes: int = [i for i in range(number_of_diodes)]

    def __getitem__(self, index: int) -> int:
        return self.diodes[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.diodes[index] = value

    def show(self) -> None:
        pass