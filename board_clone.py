from pieces import *
from typing import Union


class Board:
    """Board class"""

    squares: list

    def __init__(self):
        """
        Initializes a board with a set of squares.
        """
        self.squares = [[None for _ in range(8)] for _ in range(8)]

        # Initialize the board with pieces
        self.squares[0][0] = Rook("a8", Color.BLACK)
        self.squares[0][1] = Knight("b8", Color.BLACK)
        self.squares[0][2] = Bishop("c8", Color.BLACK)
        self.squares[0][3] = Queen("d8", Color.BLACK)
        self.squares[0][4] = King("e8", Color.BLACK)
        self.squares[0][5] = Bishop("f8", Color.BLACK)
        self.squares[0][6] = Knight("g8", Color.BLACK)
        self.squares[0][7] = Rook("h8", Color.BLACK)
        for i in range(8):
            self.squares[1][i] = Pawn(chr(ord("a") + i) + "7", Color.BLACK)

        self.squares[7][0] = Rook("a1", Color.WHITE)
        self.squares[7][1] = Knight("b1", Color.WHITE)
        self.squares[7][2] = Bishop("c1", Color.WHITE)
        self.squares[7][3] = Queen("d1", Color.WHITE)
        self.squares[7][4] = King("e1", Color.WHITE)
        self.squares[7][5] = Bishop("f1", Color.WHITE)
        self.squares[7][6] = Knight("g1", Color.WHITE)
        self.squares[7][7] = Rook("h1", Color.WHITE)
        for i in range(8):
            self.squares[6][i] = Pawn(chr(ord("a") + i) + "2", Color.WHITE)

    def get_piece(self, pos: str) -> Union[Piece, None]:
        """
        Returns the piece at the given position.
        """
        row, col = get_row_col(pos)
        return self.squares[row][col]

    def match_color(self, target: str, color: Color) -> bool:
        """
        Returns True if the piece at the target position is the same color as the given color.
        """
        piece = self.get_piece(target)
        if piece is None:
            return False
        return piece.color == color

    # Update board stuff
    def get_en_passant_piece(self, target: str, color: Color) -> Union[Pawn, None]:
        """
        Returns the pawn that is en passant.
        """
        if color == Color.WHITE:
            # The white pawn can only en passant the opponent's pawn at the 6th rank
            if int(target[1]) == 6:
                eaten_square: str = target[0] + "5"
                eaten_piece: Piece = self.get_piece(eaten_square)
                if (
                    eaten_piece is not None
                    and isinstance(eaten_piece, Pawn)
                    and eaten_piece.color == Color.BLACK
                    and eaten_piece.jump
                ):
                    return eaten_piece
        else:
            # The black pawn can only en passant the opponent's pawn at the 3rd rank
            if int(target[1]) == 3:
                eaten_square: str = target[0] + "4"
                eaten_piece: Piece = self.get_piece(eaten_square)
                if (
                    eaten_piece is not None
                    and isinstance(eaten_piece, Pawn)
                    and eaten_piece.color == Color.WHITE
                    and eaten_piece.jump
                ):
                    return eaten_piece
        return None

    def get_piece_eaten_by_pawn(self, pawn: Pawn, target: str) -> Union[Piece, None]:
        """
        - Returns the piece that the pawn at the given position will eat.
        - This can only be called if the pawn moves diagonally
        """
        row, col = get_row_col(target)
        if self.squares[row][col] is not None:
            return self.squares[row][col]
        # If not then the pawn might en passant
        return self.get_en_passant_piece(target, pawn.color)

    def update_rook_when_castle(self, king_target: str) -> None:
        """
        - Updates the rook when the king castles.
        - :param king_target: The target square to castle.
        """
        if king_target[0] == "g":
            rook_pos = "h" + king_target[1]
            rook_target = "f" + king_target[1]
        else:
            rook_pos = "a" + king_target[1]
            rook_target = "d" + king_target[1]
        rook: Union[Piece, None] = self.get_piece(rook_pos)
        if rook is not None:
            rook.pos = rook_target

    def update_board(self, piece: Piece, target: str, castle: bool = False) -> None:
        """
        - Updates the board with the given piece at the target position.
        - :param piece: The piece to be moved.
        - :param target: The target position which is validated.
        """
        if isinstance(piece, Pawn):
            if piece.move_diagonally(target):
                square_to_eat: str = self.get_piece_eaten_by_pawn(piece, target).pos
                self.squares[get_row_col(square_to_eat)[0]][
                    get_row_col(square_to_eat)[1]
                ] = None
        if castle:
            self.update_rook_when_castle(target)
        row, col = get_row_col(target)
        self.squares[row][col] = piece
        start_row, start_col = get_row_col(piece.pos)
        self.squares[start_row][start_col] = None
        piece.pos = target


def get_row_col(pos: str) -> tuple[int]:
    """Returns the row and column of the given position."""
    col = ord(pos[0]) - ord("a")
    row = 8 - int(pos[1])
    return row, col
