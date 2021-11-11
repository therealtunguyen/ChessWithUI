import chess_items
import pygame
from pieces import *


def choose_piece(piece: Piece):
    if piece.color == Color.WHITE:
        if isinstance(piece, Pawn):
            return pygame.transform.scale(chess_items.WHITE_PAWN, (70, 70))
        elif isinstance(piece, Rook):
            return pygame.transform.scale(chess_items.WHITE_ROOK, (70, 70))
        elif isinstance(piece, Knight):
            return pygame.transform.scale(chess_items.WHITE_KNIGHT, (70, 70))
        elif isinstance(piece, Bishop):
            return pygame.transform.scale(chess_items.WHITE_BISHOP, (70, 70))
        elif isinstance(piece, Queen):
            return pygame.transform.scale(chess_items.WHITE_QUEEN, (70, 70))
        elif isinstance(piece, King):
            return pygame.transform.scale(chess_items.WHITE_KING, (70, 70))
    else:
        if isinstance(piece, Pawn):
            return pygame.transform.scale(chess_items.BLACK_PAWN, (70, 70))
        elif isinstance(piece, Rook):
            return pygame.transform.scale(chess_items.BLACK_ROOK, (70, 70))
        elif isinstance(piece, Knight):
            return pygame.transform.scale(chess_items.BLACK_KNIGHT, (70, 70))
        elif isinstance(piece, Bishop):
            return pygame.transform.scale(chess_items.BLACK_BISHOP, (70, 70))
        elif isinstance(piece, Queen):
            return pygame.transform.scale(chess_items.BLACK_QUEEN, (70, 70))
        elif isinstance(piece, King):
            return pygame.transform.scale(chess_items.BLACK_KING, (70, 70))
