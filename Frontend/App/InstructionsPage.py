import os

import pygame

from Frontend.App.ScreenHandler import ScreenHandler


class InstructionsPage:
    def __init__(self, screen_handler):
        self.screen_handler = screen_handler

        self.title_font = pygame.font.Font(None, 80)
        self.heading_font = pygame.font.Font(None, 50)
        self.text_font = pygame.font.Font(None, 28)

        # Define text content
        self.instructions = [
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

    # Function to render text blocks on screen
    def render_text(self, screen, text_blocks, y_start, y_gap):
        y = y_start
        for block in text_blocks:
            if block["is_heading"]:
                title = self.heading_font.render(block["title"], True, self.screen_handler.WHITE)
                screen.blit(title, (50, y))
                y += title.get_height() + 10

            wrapped_content = ScreenHandler.wrap_text(self.text_font, block["content"],
                                                      self.screen_handler.SCREEN_WIDTH - 100)
            for line in wrapped_content:
                content_line = self.text_font.render(line, True, self.screen_handler.WHITE)
                screen.blit(content_line, (50, y))
                y += content_line.get_height() + 5

            y += y_gap  # Gap between blocks

    def run(self):
        current_file_path = __file__
        image_path = os.path.dirname(current_file_path) + "\\Background_Images\\Instructions_Background.jpg"
        # Load background image
        bg_image = pygame.image.load(
            image_path)
        bg_image = pygame.transform.scale(bg_image,
                                          (self.screen_handler.SCREEN_WIDTH, self.screen_handler.SCREEN_HEIGHT))

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
            self.screen_handler.screen.blit(bg_image, (0, 0))

            # Render the "Instructions" title
            instructions_title = self.title_font.render("Instructions", True, self.screen_handler.WHITE)
            self.screen_handler.screen.blit(instructions_title,
                                            ((self.screen_handler.SCREEN_WIDTH - instructions_title.get_width()) / 2,
                                             50))

            # Render text blocks
            self.render_text(self.screen_handler.screen, self.instructions, 150, 50)

            # Update the display
            pygame.display.flip()
