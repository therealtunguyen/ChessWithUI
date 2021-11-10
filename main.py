from pieces import *
from board import Board
from typing import Union


def validate_piece(current_player: Color, board: Board) -> tuple[Piece, str]:
    """Validating the chosen square"""
    chosen_square: str = input("Choose a square to move: ")
    piece: Union[Piece, None] = board.get_piece(chosen_square)

    # Make a while loop until the piece is valid
    while piece is None or piece.color != current_player:
        if piece is None:
            print("No piece on that square")
        elif piece.color != current_player:
            print("That piece is not yours")
        chosen_square = input("Choose a square to move: ")
        piece = board.get_piece(chosen_square)
    return (piece, chosen_square)


def promotion() -> Union[type, None]:
    print("Choose a number corresponding to a piece that you would like to promote!")
    print("1. Queen   2. Rook   3. Bishop   4. Knight")
    choice: int = int(input("Choice: "))
    if choice == 1:
        return Queen
    elif choice == 2:
        return Rook
    elif choice == 3:
        return Bishop
    elif choice == 4:
        return Knight
    return None


def move_piece_on_board(board: Board, piece: Piece, chosen_square: str, target_square: str) -> bool:
    """Move the piece on the board"""
    is_a_pawn: bool = isinstance(piece, Pawn)
    is_a_king: bool = isinstance(piece, King)
    promote_type = None
    if is_a_pawn:  # Check for promotion
        if piece.can_promote(target_square):
            promote_type = promotion()
    if is_a_king:
        do_castle: bool = piece.castle(target_square)
    board.update(chosen_square, target_square, is_pawn=is_a_pawn, do_castle=(is_a_king and do_castle))
    piece.pos = target_square
    if promote_type is not None:
        promote_piece_row, promote_piece_col = board.get_row_col(target_square)
        board.squares[promote_piece_row][promote_piece_col] = promote_type(target_square, piece.color)
    if board.can_check(board.get_piece(target_square)):
        print("Check!")
        return True
    return False


def able_to_move_on_board(chosen_square: str, target_square: str, board: Board) -> bool:
    """
    - Moving the piece
    - Return True if moving the piece is successful
    """
    # Note that updating the board does not affect the pos attribute of the piece
    valid_moves: list[str] = board.get_valid_moves(chosen_square)
    if target_square in valid_moves:
        return True
    else:
        return False


def main() -> None:
    board = Board()
    current_player: Color = Color.WHITE

    while True:
        # Print the chess board
        print(board)

        # Get player inputs
        piece: Piece
        chosen_square: str
        piece, chosen_square = validate_piece(current_player, board)
        target_square: str = input(f"Where would you like to move from {chosen_square} to: ")

        # Move the piece
        if able_to_move_on_board(chosen_square, target_square, board):
            print(f"Moving from {chosen_square} to {target_square}...")
            # If check
            if move_piece_on_board(board, piece, chosen_square, target_square):
                if board.checkmate(board.get_opposite_color(piece.color)):
                    print(f"Checkmate! {piece.color} wins!")
                    break
            else:  #  If not check
                if board.stalemate(board.get_opposite_color(piece.color)):
                    print("Stalemate!")
                    break
            # Change the current player's color
            current_player = Color.BLACK if current_player == Color.WHITE else Color.WHITE
        else:
            print("Invalid move")
        print()


if __name__ == "__main__":
    main()
