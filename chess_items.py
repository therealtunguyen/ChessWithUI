import pygame
import os

# Chess board
CHESS_BOARD_IMG = pygame.image.load(os.path.join("images", "board.png"))
CHESS_BOARD = pygame.transform.scale(CHESS_BOARD_IMG, (600, 600))

# Chess pieces
WHITE_PAWN = pygame.image.load(os.path.join("images", "white-pawn.png"))
WHITE_ROOK = pygame.image.load(os.path.join("images", "white-rook.png"))
WHITE_KNIGHT = pygame.image.load(os.path.join("images", "white-knight.png"))
WHITE_BISHOP = pygame.image.load(os.path.join("images", "white-bishop.png"))
WHITE_QUEEN = pygame.image.load(os.path.join("images", "white-queen.png"))
WHITE_KING = pygame.image.load(os.path.join("images", "white-king.png"))

BLACK_PAWN = pygame.image.load(os.path.join("images", "black-pawn.png"))
BLACK_ROOK = pygame.image.load(os.path.join("images", "black-rook.png"))
BLACK_KNIGHT = pygame.image.load(os.path.join("images", "black-knight.png"))
BLACK_BISHOP = pygame.image.load(os.path.join("images", "black-bishop.png"))
BLACK_QUEEN = pygame.image.load(os.path.join("images", "black-queen.png"))
BLACK_KING = pygame.image.load(os.path.join("images", "black-king.png"))
