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

def have_winner(board: Board) -> bool:
    """Checking if there is a winner"""
    if board.check_mate(Color.WHITE):
        print("Black wins!")
        return True
    elif board.check_mate(Color.BLACK):
        print("White wins!")
        return True
    return False

def moving_piece(board: Board, piece: Piece, chosen_square: str, target_square: str) -> bool:
    """
    - Check if there the piece moves to its color, update the board if it doesn't
    - Return False if the piece moves to its color
    """
    if board.match_color(target_square, piece.color):
        return False
    else:
        board.update(chosen_square, target_square)
        piece.pos = target_square
        return True

def able_to_move_on_board(chosen_square: str, target_square: str,piece: Piece, board: Board) -> bool:
    """
    - Moving the piece
    - Return True if moving the piece is successful
    """
    # Note that updating the board does not affect the pos attribute of the piece
    if piece.can_move(target_square):
        # Check if the piece is a pawn because it has special rules called en passant
        if isinstance(piece, Pawn):
            if board.en_pas(chosen_square, target_square, piece.color):
                return moving_piece(board, piece, chosen_square, target_square)
        # Check if the piece is a king because it has special rules called castling
        elif isinstance(piece, King):
            if board.castle(chosen_square, target_square, piece.color):
                return moving_piece(board, piece, chosen_square, target_square)
        else:
            return moving_piece(board, piece, chosen_square, target_square)
    else:
        print("Invalid move\n")
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
        if able_to_move_on_board(chosen_square, target_square, piece, board):
            print(f"Moving from {chosen_square} to {target_square}...\n")
            # Change the current player's color
            current_player = Color.BLACK if current_player == Color.WHITE else Color.WHITE
        else:
            print("Invalid move\n")


if __name__ == "__main__":
    main()