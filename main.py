from pieces import *
from board import Board
import time

def validate_piece(current_player: Color) -> tuple[Piece, str]:
    """Validating the chosen square"""
    chosen_square: str = input("Choose a square to move: ")
    piece: Piece = board.get_piece(chosen_square)
    
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

def move(chosen_square: str, target_square: str,piece: Piece, board: Board) -> None:
    """
    - Moving the piece
    - Note that updating the board does not affect the pos attribute of the piece
    """
    # Check if the piece is a pawn because it has special rules like en passant
    if isinstance(piece, Pawn):
        if board.pawn_can_move(chosen_square, target_square, piece.color):
            if board.match_color(target_square, piece.color):
                print("You cannot move to your own piece")
            else:
                board.update(chosen_square, target_square, is_pawn=True)
                piece.pos = target_square
    # Check if the piece is a king because it has special rules like castling
    elif isinstance(piece, King):
        print("Is King")
        if board.king_can_move(chosen_square, target_square, piece.color):
            if board.match_color(target_square, piece.color):
                print("You cannot move to your own piece")
            else:
                board.update(chosen_square, target_square)
                piece.pos = target_square
    elif piece.can_move(target_square):
        if board.match_color(target_square, piece.color):
            print("You cannot move to your own piece")
        else:
            board.update(chosen_square, target_square)
            piece.pos = target_square
    else:
        print("Invalid move")

board = Board()
current_player: Color = Color.WHITE

while True:
    # Print the chess board
    print(board)

    # Get player inputs
    piece: Piece
    chosen_square: str
    piece, chosen_square = validate_piece(current_player)
    target_square: str = input(f"Where would you like to move from {chosen_square} to: ")

    # Some decoration
    time.sleep(0.25)
    print(f"Moving from {chosen_square} to {target_square}...\n")

    # Move the piece
    move(chosen_square, target_square, piece, board)

    # Change the current player's color
    current_player = Color.BLACK if current_player == Color.WHITE else Color.WHITE
    time.sleep(0.5)