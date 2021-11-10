"""Make chess pieces"""
from abc import ABC, abstractmethod
from enum import Enum, auto


class Color(Enum):
    """Color of a piece"""

    WHITE = auto()
    BLACK = auto()


class Piece(ABC):
    symbol: str = "?"

    """Abstract class for chess pieces"""

    def __init__(self, pos: str, color: Color) -> None:
        self.pos: str = pos
        self.color: Color = color

    def __repr__(self) -> str:
        return f"Piece: {self.symbol} {self.color}"

    def square_in_board(self, target: str) -> bool:
        """Check if the target square is on the board or not"""
        letter, number = target[0], target[1]
        if letter.isalpha() and number.isnumeric():
            if letter in "abcdefgh" and number in "12345678":
                return True
        return False

    @abstractmethod
    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""


class Rook(Piece):
    """Rook class"""

    has_castled = False

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wR" if self.color == Color.WHITE else "bR"

    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""
        if self.square_in_board(target):
            if target[0] == self.pos[0] or target[1] == self.pos[1]:
                return True
        return False


class Bishop(Piece):
    """Bishop class"""

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wB" if self.color == Color.WHITE else "bB"

    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""
        if self.square_in_board(target):
            if abs(ord(target[0]) - ord(self.pos[0])) == abs(int(target[1]) - int(self.pos[1])):
                return True
        return False


class Queen(Piece):
    """Queen class"""

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wQ" if self.color == Color.WHITE else "bQ"

    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""
        if self.square_in_board(target):
            if target[0] == self.pos[0] or target[1] == self.pos[1]:
                return True
            elif abs(ord(target[0]) - ord(self.pos[0])) == abs(int(target[1]) - int(self.pos[1])):
                return True
        return False


class King(Piece):
    """King class"""

    has_castled = False

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wK" if self.color == Color.WHITE else "bK"

    def castle(self, target: str) -> bool:
        """Return True if the king wants to castle and do not care whether it is a valid move"""
        if self.square_in_board(target):
            if target[1] == self.pos[1] and abs(ord(target[0]) - ord(self.pos[0])) == 2:
                return True
        return False

    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""
        if self.square_in_board(target):
            if abs(ord(target[0]) - ord(self.pos[0])) <= 1 and abs(int(target[1]) - int(self.pos[1])) <= 1:
                return True
            elif target[1] == self.pos[1] and abs(ord(target[0]) - ord(self.pos[0])) == 2 and not self.has_castled:
                return True
        return False


class Knight(Piece):
    """Knight class"""

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wN" if self.color == Color.WHITE else "bN"

    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""
        if self.square_in_board(target):
            if abs(ord(target[0]) - ord(self.pos[0])) == 2 and abs(int(target[1]) - int(self.pos[1])) == 1:
                return True
            elif abs(ord(target[0]) - ord(self.pos[0])) == 1 and abs(int(target[1]) - int(self.pos[1])) == 2:
                return True
        return False


class Pawn(Piece):
    """Pawn class"""

    jump = False  # If the pawn moves two squares, jump will be True

    def __init__(self, pos: str, color: Color) -> None:
        super().__init__(pos, color)
        self.symbol = "wP" if self.color == Color.WHITE else "bP"

    def move_diagonal(self, target: str, color: Color) -> bool:
        """Check if the pawn is moving diagonally"""
        if color == Color.WHITE:
            if abs(ord(target[0]) - ord(self.pos[0])) == 1:
                if int(target[1]) - int(self.pos[1]) == 1:
                    return True
        else:
            if abs(ord(target[0]) - ord(self.pos[0])) == 1:
                if int(target[1]) - int(self.pos[1]) == -1:
                    return True
        return False

    def can_promote(self, target: str) -> bool:
        """Return True if the pawn is able to promote"""
        if self.color == Color.WHITE:
            if target[1] == "8":
                return True
        else:
            if target[1] == "1":
                return True
        return False

    def can_move(self, target: str) -> bool:
        """Return True if the piece can move to the target and do not care whether it is valid"""
        if self.square_in_board(target):
            if self.color == Color.WHITE:
                if target[0] == self.pos[0]:
                    if int(target[1]) - int(self.pos[1]) == 1:
                        return True
                    elif int(target[1]) - int(self.pos[1]) == 2 and self.pos[1] == "2":
                        self.jump = True
                        return True
                else:
                    return self.move_diagonal(target, self.color)  # Capture diagonally
            elif self.color == Color.BLACK:
                if target[0] == self.pos[0]:
                    if int(target[1]) - int(self.pos[1]) == -1:
                        return True
                    elif int(target[1]) - int(self.pos[1]) == -2 and self.pos[1] == "7":
                        self.jump = True
                        return True
                else:
                    return self.move_diagonal(target, self.color)  # Capture diagonally
        return False
