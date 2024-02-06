from PieceSprite import PieceSprite
from board import Board
import pygame


class GUIHandler:
    def __init__(self):
        self.color = (255, 255, 255)
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.board = Board(screen)
        self.board.create_board(self.color)
