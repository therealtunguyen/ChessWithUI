from pieces import *
from typing import Union

class Board:
    """
    A class that represents a chess board.
    """
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
            self.squares[1][i] = Pawn(chr(ord("a") + i) + '7', Color.BLACK)

        self.squares[7][0] = Rook("a1", Color.WHITE)
        self.squares[7][1] = Knight("b1", Color.WHITE)
        self.squares[7][2] = Bishop("c1", Color.WHITE)
        self.squares[7][3] = Queen("d1", Color.WHITE)
        self.squares[7][4] = King("e1", Color.WHITE)
        self.squares[7][5] = Bishop("f1", Color.WHITE)
        self.squares[7][6] = Knight("g1", Color.WHITE)
        self.squares[7][7] = Rook("h1", Color.WHITE)
        for i in range(8):
            self.squares[6][i] = Pawn(chr(ord("a") + i) + '2', Color.WHITE)

    def __repr__(self):
        """Displays the board."""
        board = "=" * 25 + "\n"
        for row in range(8):
            board += f"{8 - row} "
            for col in range(8):
                piece: Piece = self.squares[row][col]
                if piece is not None:
                    board += f"{piece.symbol} "
                else:
                    board += "   "
            board += "\n"
        board += "  a  b  c  d  e  f  g  h" + "\n" + "=" * 25
        return board

    def get_row_col(self, pos: str) -> tuple[int]:
        """Returns the row and column of the given position."""
        col = ord(pos[0]) - ord("a")
        row = 8 - int(pos[1])
        return row, col

    def get_square_name(self, row: int, col: int) -> str:
        """Returns the name of the square at the given row and column."""
        return chr(ord("a") + col) + str(8 - row)

    def get_piece(self, pos: str) -> Union[Piece, None]:
        """Returns the piece at the given position."""
        row, col = self.get_row_col(pos)
        return self.squares[row][col]

    def match_color(self, target: str, current_color: Color) -> bool:
        """Returns True if the piece at the given position is of the given color."""
        piece = self.get_piece(target)
        if piece is None:
            return False
        return piece.color == current_color

    def en_pas(self, pos: str, target: str, color: Color) -> Union[str, bool]:
        """
        - This can only be called if the piece at pos is a pawn.
        - Return the square that is captured by the pawn if it moves diagonally
        - Return the target square if the pawn move forward
        - Return False if the pawn can't move diagonally.
        """
        pawn: Pawn = self.get_piece(pos)
        if pawn.move_diagonal(target, color):
            if color == Color.WHITE:
                if self.get_piece(target) is not None:  # Pawn can only capture if there is a piece there
                    return target
                # Check the en passant case
                elif int(target[1]) - 1 == 5:  # Which is the only way to en passant
                    en_passant: str = target[0] + str(int(target[1]) - 1)
                    en_passant_square: Union[Pawn, None] = self.get_piece(en_passant)
                    if en_passant_square is not None and isinstance(en_passant_square, Pawn):
                        if en_passant_square.jump:
                            return en_passant
                return False
            else:
                if self.get_piece(target) is not None:
                    return target
                elif int(target[1]) + 1 == 4:
                    en_passant: str = target[0] + str(int(target[1]) + 1)
                    en_passant_square: Union[Pawn, None] = self.get_piece(en_passant)
                    if en_passant_square is not None and isinstance(en_passant_square, Pawn):
                        if en_passant_square.jump:
                            return en_passant
                return False
        target_piece: Piece = self.get_piece(target)
        if target_piece is not None:  # Pawn can't move forward
            return False
        return target

    def castle(self, pos: str, target: str, color: Color) -> bool:
        """
        - This can only be called if the piece at pos is a king.
        - If the king castles, update the rook position and return True.
        - If it can't castle return False.
        """
        king: King = self.get_piece(pos)
        if king.castle(target):
            rook_pos = 'a' if target[0] == 'c' else 'h'
            rook_target = 'd' if target[0] == 'c' else 'f'
            if color == Color.WHITE:
                rook_pos += '1'
                rook_target += '1'
            else:
                rook_pos += '8'
                rook_target += '8'
            
            rook: Union[Rook, None] = self.get_piece(rook_pos)
            if rook is None:
                return False
            elif not king.has_castled and not rook.has_castled:
                # Update the rook position
                self.update(rook_pos, rook_target)
                rook.pos = rook_target
                # rook.has_castled = True
                # king.has_castled = True
                return True
            return False
        # king.has_castled = True
        return True

    def keep_checking(self, color: Color, index: tuple[int], direction: tuple[int]) -> list[str]:
        """Keep checking valid squares"""
        original_pos: str = self.get_square_name(*index)
        row_target: int
        col_target: int
        row_target, col_target = index
        valid_squares: list = []
        has_eaten: bool = False
        while not has_eaten:
            row_target += direction[0]
            col_target += direction[1]
            if row_target < 0 or row_target > 7 or col_target < 0 or col_target > 7:
                break
            else:
                target: str = self.get_square_name(row_target, col_target)
                target_piece: Union[Piece, None] = self.get_piece(target)
                if not self.get_piece(original_pos).can_move(target):
                    break
                elif target_piece is not None:
                    if self.match_color(target, color):
                        break
                    elif not self.match_color(target, color):
                        has_eaten = True
                valid_squares.append(target)
        return valid_squares

    def get_valid_moves_for_knights(self, pos: str) -> list[str]:
        """Returns a list of valid squares for the knight at the given position."""
        # Loop through all the squares and append to the list if it is valid
        valid_squares: list = []
        knight: Knight = self.get_piece(pos)
        for i in range(8):
            for j in range(8):
                target: str = self.get_square_name(i, j)
                if knight.can_move(target) and not self.match_color(target, knight.color):
                    valid_squares.append(target)
        return valid_squares

    def get_valid_moves(self, pos: str) -> list[str]:
        """
        - Check and return the valid piece's available squares
        - Only use for piece that isn't a knight
        """
        if isinstance(self.get_piece(pos), Knight):
            return self.get_valid_moves_for_knights(pos)
        orders: list[list[int]] = [
            [-1, 0], [-1, 1], [0, 1], [1, 1],
            [1, 0], [1, -1], [0, -1], [-1, -1]
        ]
        row: int
        col: int
        row, col = self.get_row_col(pos)
        piece: Piece = self.squares[row][col]
        available_squares: list = []
        
        for order in orders:
            row_order = row + order[0]
            col_order = col + order[1]
            if row_order < 0 or row_order > 7 or col_order < 0 or col_order > 7:
                continue
            target: str = self.get_square_name(row_order, col_order)
            if piece.can_move(target):
                if isinstance(piece, Pawn):  # Check for en passant case
                    if self.en_pas(pos, target, piece.color) is not False:
                        available_squares.extend(self.keep_checking(piece.color, (row, col), (order[0], order[1])))
                elif isinstance(piece, King):  # Check for castle case
                    if self.castle(pos, target, piece.color):
                        available_squares.extend(self.keep_checking(piece.color, (row, col), (order[0], order[1])))
                else:
                    available_squares.extend(self.keep_checking(piece.color, (row, col), (order[0], order[1])))
        return available_squares

    def update(self, pos: str, target: str, is_pawn: bool = False, do_castle: bool = False) -> None:
        """Update chess board by moving the piece to the target position."""
        if is_pawn:
            captured_square = self.en_pas(pos, target, self.get_piece(pos).color)
            captured_row, captured_col = self.get_row_col(captured_square)
            self.squares[captured_row][captured_col] = None
        if do_castle:
            rook_pos = 'a' + target[1] if target[0] == 'c' else 'h'
            rook: Rook = self.get_piece(rook_pos)
            rook.pos = 'd' + target[1] if target[0] == 'c' else 'f'
            rook.has_castled = True
            self.get_piece(pos).has_castled = True
        
        pos_row, pos_col = self.get_row_col(pos)
        target_row, target_col = self.get_row_col(target)
        self.squares[target_row][target_col] = self.squares[pos_row][pos_col]
        self.squares[pos_row][pos_col] = None