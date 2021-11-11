from pieces import *
from board import *
from typing import Union


def validate_piece(current_player: Color, board: Board) -> tuple[Piece, str, list[str]]:
    """Validating the chosen square"""
    chosen_square: str = input("Choose a square to move: ")
    piece: Union[Piece, None] = board.get_piece(chosen_square)

    # Make a while loop until the piece is valid
    while True:
        if piece is None:
            print("No piece on that square")
        elif piece.color != current_player:
            print("That piece is not yours")
        else:
            piece_moves: list[str] = board.get_valid_moves(chosen_square)
            actual_piece_moves: list[str] = board.process_target(piece, piece_moves)
            if len(actual_piece_moves) == 0:
                print("That piece cannot move because you will be in check!")
            else:
                break
        chosen_square = input("Choose a square to move: ")
        piece = board.get_piece(chosen_square)
    return (piece, chosen_square, actual_piece_moves)


def validate_target(board: Board, piece: Piece, piece_moves: list[str]) -> str:
    """Validating the target square"""
    target_square: str = input("Choose a square to move to: ")
    while True:
        if board.get_checked_when_move(piece, target_square):
            print("That move will put you in check!")
        elif target_square not in piece_moves:
            print("That move is not valid")
        else:
            break
        target_square = input("Choose a square to move to: ")
    return target_square


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


def move_piece_on_board(
    board: Board, piece: Piece, chosen_square: str, target_square: str
) -> bool:
    """Move the piece on the board"""
    is_a_pawn: bool = isinstance(piece, Pawn)
    is_a_king: bool = isinstance(piece, King)
    promote_type = None
    if is_a_pawn:  # Check for promotion
        if piece.can_promote(target_square):
            promote_type = promotion()
    if is_a_king:
        do_castle: bool = piece.castle(target_square)
    board.update(
        chosen_square,
        target_square,
        is_pawn=is_a_pawn,
        do_castle=(is_a_king and do_castle),
    )
    piece.pos = target_square
    if promote_type is not None:
        promote_piece_row, promote_piece_col = board.get_row_col(target_square)
        board.squares[promote_piece_row][promote_piece_col] = promote_type(
            target_square, piece.color
        )
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


def validate_player_input(current_player: Color, board: Board) -> tuple[Piece, str]:
    """Get the valid input from player"""
    piece: Piece
    chosen_square: str
    piece, chosen_square, valid_moves = validate_piece(current_player, board)
    target_square: str = validate_target(board, piece, valid_moves)
    return (piece, chosen_square, target_square)


def main() -> None:
    board = Board()
    current_player: Color = Color.WHITE

    while True:
        # Print the chess board
        print(board)

        # Get player inputs
        piece: Piece
        chosen_square: str
        target_square: str
        piece, chosen_square, target_square = validate_player_input(current_player, board)

        # Move the piece
        print(f"Moving from {chosen_square} to {target_square}...")
        # If check
        if move_piece_on_board(board, piece, chosen_square, target_square):
            moves_to_cover_check: list = board.move_to_not_mate(
                get_opposite_color(piece.color)
            )
            king_moves_to_live: list = board.get_valid_moves(
                board.get_king_pos(get_opposite_color(piece.color))
            )
            # If there are moves to cover check
            if moves_to_cover_check:
                # Extend with the king's moves
                moves_to_cover_check.extend(king_moves_to_live)
            else:  # If there are no moves to cover check
                if not king_moves_to_live:
                    print(board)
                    print("Checkmate!")
                    break
        else:  #  If not check
            if board.stalemate(get_opposite_color(piece.color)):
                print("Stalemate!")
                break
        # Change the current player's color
        current_player = Color.BLACK if current_player == Color.WHITE else Color.WHITE


if __name__ == "__main__":
    main()
