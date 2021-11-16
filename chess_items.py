import pygame
from pygame import Surface
import os

# Chess board
CHESS_BOARD_IMG: Surface = pygame.image.load(os.path.join("images", "chess-board.png"))
CHESS_BOARD: Surface = pygame.transform.scale(CHESS_BOARD_IMG, (600, 600))

# Chess pieces
WHITE_PAWN: Surface = pygame.image.load(os.path.join("images", "white-pawn.png"))
WHITE_ROOK: Surface = pygame.image.load(os.path.join("images", "white-rook.png"))
WHITE_KNIGHT: Surface = pygame.image.load(os.path.join("images", "white-knight.png"))
WHITE_BISHOP: Surface = pygame.image.load(os.path.join("images", "white-bishop.png"))
WHITE_QUEEN: Surface = pygame.image.load(os.path.join("images", "white-queen.png"))
WHITE_KING: Surface = pygame.image.load(os.path.join("images", "white-king.png"))

BLACK_PAWN: Surface = pygame.image.load(os.path.join("images", "black-pawn.png"))
BLACK_ROOK: Surface = pygame.image.load(os.path.join("images", "black-rook.png"))
BLACK_KNIGHT: Surface = pygame.image.load(os.path.join("images", "black-knight.png"))
BLACK_BISHOP: Surface = pygame.image.load(os.path.join("images", "black-bishop.png"))
BLACK_QUEEN: Surface = pygame.image.load(os.path.join("images", "black-queen.png"))
BLACK_KING: Surface = pygame.image.load(os.path.join("images", "black-king.png"))

# Icons
FLIP_ICON: Surface = pygame.transform.scale(
    pygame.image.load(os.path.join("images", "flip-board.png")), (28, 28)
)
ON_BUTTON: Surface = pygame.image.load(os.path.join("images", "on-button.png"))
OFF_BUTTON: Surface = pygame.image.load(os.path.join("images", "off-button.png"))
