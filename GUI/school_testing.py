import pygame

color = (255, 255, 255)
pygame.init()

screen = pygame.display.set_mode((255, 255))


class Board:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.margin = 5

    def create_board(self):
        for column in range(10):
            for row in range(10):
                pygame.draw.rect(screen, color,
                                 pygame.Rect(column * (self.width + self.margin) + self.margin,
                                             row * (self.height + self.margin) +
                                             self.margin, self.width, self.height))


board = Board()
board.create_board()
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            # Toggle fullscreen mode
            pygame.display.toggle_fullscreen()
pygame.quit()
