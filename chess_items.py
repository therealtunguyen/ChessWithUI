import pygame
from pygame import Surface
import os

pygame.mixer.init()

# Chess board
CHESS_BOARD_IMG: Surface = pygame.image.load(os.path.join("Assets", "chess-board.png"))
CHESS_BOARD: Surface = pygame.transform.scale(CHESS_BOARD_IMG, (600, 600))

# Chess pieces
WHITE_PAWN: Surface = pygame.image.load(os.path.join("Assets", "white-pawn.png"))
WHITE_ROOK: Surface = pygame.image.load(os.path.join("Assets", "white-rook.png"))
WHITE_KNIGHT: Surface = pygame.image.load(os.path.join("Assets", "white-knight.png"))
WHITE_BISHOP: Surface = pygame.image.load(os.path.join("Assets", "white-bishop.png"))
WHITE_QUEEN: Surface = pygame.image.load(os.path.join("Assets", "white-queen.png"))
WHITE_KING: Surface = pygame.image.load(os.path.join("Assets", "white-king.png"))

BLACK_PAWN: Surface = pygame.image.load(os.path.join("Assets", "black-pawn.png"))
BLACK_ROOK: Surface = pygame.image.load(os.path.join("Assets", "black-rook.png"))
BLACK_KNIGHT: Surface = pygame.image.load(os.path.join("Assets", "black-knight.png"))
BLACK_BISHOP: Surface = pygame.image.load(os.path.join("Assets", "black-bishop.png"))
BLACK_QUEEN: Surface = pygame.image.load(os.path.join("Assets", "black-queen.png"))
BLACK_KING: Surface = pygame.image.load(os.path.join("Assets", "black-king.png"))

# Icons
FLIP_ICON: Surface = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "flip-board.png")), (28, 28)
)
ON_BUTTON: Surface = pygame.image.load(os.path.join("Assets", "on-button.png"))
OFF_BUTTON: Surface = pygame.image.load(os.path.join("Assets", "off-button.png"))
RESET_BUTTON: Surface = pygame.image.load(os.path.join("Assets", "reset.png"))

# Sounds
MOVE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "move_sound.wav"))
