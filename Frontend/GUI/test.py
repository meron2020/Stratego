import sys
from Frontend.Game.PieceSprite import PieceSprite
import pygame

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
FPS = 60
SQUARE_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Define classes
class Piece(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        image = "Sprite_Images/soldier.png"
        self.image = pygame.transform.scale(pygame.image.load(image),
                                            (int(self.board.cell_size), int(self.board.cell_size)))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dragging = False

    def update(self):
        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()


# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stratego Setup")
clock = pygame.time.Clock()

# Create sprites
all_sprites = pygame.sprite.Group()

# Create a simple board (you can replace this with your actual board)
board = [[None for _ in range(10)] for _ in range(10)]

# Create pieces for the initial setup
for i in range(4):
    for j in range(10):
        piece = PieceSprite("Sprite_Images/soldier.png", )
        all_sprites.add(piece)
        board[i][j] = piece

# Game loop
running = True
dragging_piece = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for piece in all_sprites:
                    if piece.rect.collidepoint(event.pos):
                        dragging_piece = piece
                        dragging_piece.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_piece is not None:
                # Snap the piece to the nearest square
                row = round(dragging_piece.rect.y / SQUARE_SIZE)
                col = round(dragging_piece.rect.x / SQUARE_SIZE)
                dragging_piece.rect.topleft = (col * SQUARE_SIZE, row * SQUARE_SIZE)
                dragging_piece.dragging = False
                dragging_piece = None

    all_sprites.update()

    # Draw the board
    screen.fill(BLACK)
    for row in range(10):
        for col in range(10):
            pygame.draw.rect(screen, WHITE if (row + col) % 2 == 0 else BLACK,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw the pieces
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
