from pieces import *
from board import *
from typing import Union
import time
import pygame
import chess_items as ci

pygame.font.init()

# Screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (166, 119, 91)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

FONT = pygame.font.SysFont("comicsans", 30)
MATE_FONT = pygame.font.SysFont("comicsans", 100)
WINNER_FONT = pygame.font.SysFont("comicsans", 70)
CHECK_TEXT = FONT.render("Check!", True, RED)
CHECKMATE_TEXT = MATE_FONT.render("Checkmate!", True, RED)
STALEMATE_TEXT = MATE_FONT.render("Stalemate!", True, RED)


def draw_screen(
    board: Board,
    current_player: Color,
    piece_moves: list[str],
    draw_moves: bool,
    check: bool,
) -> None:
    SCREEN.fill(WHITE)
    SCREEN.blit(ci.CHESS_BOARD, (0, 0))

    pygame.draw.rect(SCREEN, DARK_BROWN, (600, 450, 200, 150))
    draw_current_player(current_player)
    SCREEN.blit(CHECK_TEXT, (665, 520)) if check else None

    squares = board.squares
    for row in range(len(squares)):
        for col in range(len(squares[row])):
            piece: Union[Piece, None] = squares[row][col]
            if piece is not None:
                if piece.is_clicked:
                    pygame.draw.rect(SCREEN, YELLOW, (col * 75, row * 75, 75, 75))
                SCREEN.blit(piece.img, (col * 75, row * 75))
    if draw_moves:
        draw_available_moves(piece_moves)
    pygame.display.update()


def draw_winner(current_player: Color, is_checkmate: bool) -> None:
    if is_checkmate:
        SCREEN.blit(CHECKMATE_TEXT, (100, 200))
    else:
        SCREEN.blit(STALEMATE_TEXT, (100, 200))
    color_text = "White" if current_player == Color.WHITE else "Black"
    winner_text = WINNER_FONT.render(f"{color_text} player wins!!!", True, BLACK)
    SCREEN.blit(winner_text, (90, 300))
    pygame.display.update()


def draw_available_moves(piece_moves: list[str]) -> None:
    """Draw the available moves on the board"""
    for move in piece_moves:
        row, col = get_row_col(move)
        pygame.draw.circle(SCREEN, DARK_BROWN, (col * 75 + 37, row * 75 + 37), 10)


def draw_current_player(current_player: Color) -> None:
    current_text = FONT.render("Current Player", True, WHITE)
    player: str = "White" if current_player == Color.WHITE else "Black"
    color_of_player = WHITE if current_player == Color.WHITE else BLACK
    current_player_text = FONT.render(player, True, color_of_player)
    SCREEN.blit(current_text, (630, 460))
    SCREEN.blit(current_player_text, (670, 490))


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


def validate_chosen_piece(current_player: Color, board: Board, index: tuple[int]) -> bool:
    """Validating the chosen square"""
    piece: Union[Piece, None] = board.squares[index[0]][index[1]]

    if piece is None:
        return False
    elif piece.color != current_player:
        return False
    else:
        piece_moves: list[str] = board.get_valid_moves(piece.pos)
        actual_piece_moves: list[str] = board.process_target(piece, piece_moves)
        if len(actual_piece_moves) == 0:
            return False
    return True


def get_piece_moves(board: Board, piece: Piece) -> list[str]:
    """Get the valid moves of the piece"""
    piece_moves: list[str] = board.get_valid_moves(piece.pos)
    actual_piece_moves: list[str] = board.process_target(piece, piece_moves)
    return actual_piece_moves


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


def validate_target_piece(
    board: Board, piece: Piece, piece_moves: list[str], index: tuple[int]
) -> bool:
    """Validating the target square"""
    target_square: str = get_square_name(index[0], index[1])
    if target_square == piece.pos:
        return False
    if target_square not in piece_moves:
        return False
    if board.get_checked_when_move(piece, target_square):
        return False
    return True


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
        promote_piece_row, promote_piece_col = get_row_col(target_square)
        board.squares[promote_piece_row][promote_piece_col] = promote_type(
            target_square, piece.color
        )
    if board.can_check(board.get_piece(target_square)):
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


def main_gui():
    # Initialize the board
    board: Board = Board()
    current_player: Color = Color.WHITE
    is_choosing_target: bool = False
    can_move_piece: bool = False
    check: bool = False
    is_mate: bool = False
    is_checkmate: bool = False
    piece_moves: list[str] = []

    # Initialize the GUI
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pygame.mouse.get_pos()
                row = row // 75
                col = col // 75
                if row < 8 and col < 8:
                    if not is_choosing_target:
                        if validate_chosen_piece(current_player, board, (col, row)):
                            piece: Piece = board.squares[col][row]
                            piece.is_clicked = True
                            piece_moves: list[str] = get_piece_moves(
                                board, board.squares[col][row]
                            )
                            is_choosing_target = True
                    else:
                        is_choosing_target = False
                        if validate_target_piece(board, piece, piece_moves, (col, row)):
                            can_move_piece = True
                            target: str = get_square_name(col, row)
                            current_player = (
                                Color.BLACK
                                if current_player == Color.WHITE
                                else Color.WHITE
                            )
                        else:
                            piece.is_clicked = False
        if can_move_piece:
            king_pos: str = board.get_king_pos(get_opposite_color(piece.color))
            king: King = board.get_piece(king_pos)
            # If check
            if move_piece_on_board(board, piece, piece.pos, target):
                king.in_check = True
                check = True
                moves_to_cover_check: list = board.move_to_not_mate(
                    get_opposite_color(piece.color)
                )
                king_moves_to_live: list = board.get_valid_moves(king_pos)
                # If there are moves to cover check
                if moves_to_cover_check:
                    # Extend with the king's moves
                    moves_to_cover_check.extend(king_moves_to_live)
                else:  # If there are no moves to cover check
                    if not king_moves_to_live:
                        is_mate = True
                        is_checkmate = True
            else:  #  If not check
                king.in_check = False
                check = False
                if board.stalemate(get_opposite_color(piece.color)):
                    print("Stalemate!")
                    is_mate = True
            can_move_piece = False
            piece.is_clicked = False

        draw_screen(board, current_player, piece_moves, is_choosing_target, check)
        if is_mate:
            draw_winner(current_player, is_checkmate)
            time.sleep(5)
            running = False
    pygame.quit()


if __name__ == "__main__":
    main_gui()
