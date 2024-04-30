import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)

# Set up display in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()

pygame.display.set_caption("Stratego Instructions")

# Load background image
bg_image = pygame.image.load(
    "C:\\Users\\yoavm\\PycharmProjects\\StrategoV2\\Frontend\\Game\\Background_Images\\Instructions_Background.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Define fonts
title_font = pygame.font.Font(None, 80)
heading_font = pygame.font.Font(None, 50)
text_font = pygame.font.Font(None, 28)

# Define text content
instructions = [
    {
        "title": "Stratego",
        "content": "A two-player board game where each player commands an army. The objective is to capture the opponent's flag or eliminate their army.",
        "is_heading": True
    },
    {
        "title": "Game Setup",
        "content": ("The board is a 10x10 grid with two lakes in the center. Each player has 40 pieces: "
                    "Marshal, Generals, Colonels, and other ranks, including Miners, Scouts, and a Spy. "
                    "Bombs and a Flag are also included."),
        "is_heading": True
    },
    {
        "title": "Game Play",
        "content": ("Players take turns making one move per turn. Pieces can move one square per turn. "
                    "Special abilities: Miners defuse Bombs, Scouts move across multiple squares, "
                    "Spies defeat Marshals if they attack first."),
        "is_heading": True
    },
    {
        "title": "Winning the Game",
        "content": ("Capture the opponent's Flag or eliminate all their movable pieces to win."),
        "is_heading": True
    },
    {
        "title": "Strategies",
        "content": ("Defense: Position your Flag and Bombs strategically."
                    "Offense: Use higher-ranking pieces to eliminate key opponents. "
                    "Bluff: Mislead the opponent with low-ranking pieces or Bombs."),
        "is_heading": True
    }
]


# Function to wrap text content
def wrap_text(font, content, max_width):
    """Wraps a text content into multiple lines based on the font width."""
    words = content.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = f"{current_line} {word}"
        if font.size(test_line)[0] > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line

    lines.append(current_line)  # Append the last line
    return lines


# Function to render text blocks on screen
def render_text(screen, text_blocks, y_start, y_gap):
    y = y_start
    for block in text_blocks:
        if block["is_heading"]:
            title = heading_font.render(block["title"], True, WHITE)
            screen.blit(title, (50, y))
            y += title.get_height() + 10

        wrapped_content = wrap_text(text_font, block["content"], WIDTH - 100)
        for line in wrapped_content:
            content_line = text_font.render(line, True, WHITE)
            screen.blit(content_line, (50, y))
            y += content_line.get_height() + 5

        y += y_gap  # Gap between blocks


# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Draw the background image
    screen.blit(bg_image, (0, 0))

    # Render the "Instructions" title
    instructions_title = title_font.render("Instructions", True, WHITE)
    screen.blit(instructions_title, ((WIDTH - instructions_title.get_width()) / 2, 50))

    # Render text blocks
    render_text(screen, instructions, 150, 50)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
