import pygame

from Frontend.Game.Board import Board
from universals import PLAYER_QUIT_EVENT


class PlayerHandler:
    def __init__(self, player_id, board, screen_handler, http_handler, game_id):
        # Initialize the PlayerHandler with necessary parameters
        self.player_id = player_id
        self.board = board
        self.screen_handler = screen_handler
        self.http_handler = http_handler
        self.game_id = game_id

    def player_set_pieces(self, sprite_group):
        self.screen_handler.create_quit_button()
        clicked_sprite = None
        setup_finished = False
        self.screen_handler.present_quit_button()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == PLAYER_QUIT_EVENT:
                    return "Opponent Quit"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any sprite is clicked
                    for sprite in sprite_group:
                        if sprite.rect.collidepoint(event.pos):
                            clicked_sprite = sprite
                            clicked_sprite.start_drag(event.pos)

                    # Define the finish button rect
                    finish_button_rect = pygame.Rect(
                        pygame.display.get_window_size()[0] - 300,
                        pygame.display.get_window_size()[1] - 150,
                        175, 50
                    )
                    if finish_button_rect.collidepoint(event.pos) and setup_finished:
                        return True

                    if self.screen_handler.check_quit_button_pressed(event):
                        return False

                elif event.type == pygame.MOUSEBUTTONUP:
                    if clicked_sprite:
                        clicked_sprite.stop_drag(self.player_id)
                        clicked_sprite = None

            # Update the clicked sprite
            if clicked_sprite:
                clicked_sprite.update()

            # Update the other sprites in the group
            for sprite in sprite_group:
                if sprite != clicked_sprite:
                    sprite.update()

            # Check if player's four rows are filled
            if self.board.setup_rows_filled(self.player_id):
                # Display "Finish set up" button in the bottom right corner
                finish_button_rect = pygame.Rect(
                    pygame.display.get_window_size()[0] - 300,
                    pygame.display.get_window_size()[1] - 150,
                    175, 50
                )
                setup_finished = True

                pygame.draw.rect(self.screen_handler.screen, (0, 0, 255), finish_button_rect)
                font = pygame.font.Font(None, 36)
                text = font.render("Finish set up", True, (255, 255, 255))
                self.screen_handler.screen.blit(text, finish_button_rect.move(10, 5))
                pygame.display.flip()

            # Clear the screen
            self.screen_handler.screen.fill((255, 255, 255))

            # Draw the board and pieces
            self.board.draw_board()
            sprite_group.draw(self.screen_handler.screen)

            self.screen_handler.present_quit_button()

            # Update the display
            pygame.display.flip()

    def user_act(self, sprite_group):
        # self.screen_handler.create_quit_button()
        running = True
        possible_options = None
        clicked_piece = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                elif event.type == PLAYER_QUIT_EVENT:
                    return ["Opponent Quit"]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if self.screen_handler.check_quit_button_pressed(event):
                    #     self.http_handler.quit_game(self.game_id, self.player_id)
                    #     return [False]
                    selected_square = self.board.get_clicked_square(
                        event.pos)  # Implement this method to get the square position
                    if not possible_options:
                        piece = Board.get_clicked_sprite_and_position(sprite_group, event.pos)
                        if piece:
                            if piece.player_id == self.player_id:
                                clicked_piece = piece
                    else:
                        if selected_square in possible_options:
                            return [selected_square, clicked_piece]
                        else:
                            piece = Board.get_clicked_sprite_and_position(sprite_group, event.pos)
                            if piece:
                                if piece.player_id == self.player_id:
                                    clicked_piece = piece
            # Clear the screen
            self.screen_handler.screen.fill((255, 255, 255))
            self.board.draw_board()

            # Draw the pieces
            sprite_group.draw(self.screen_handler.screen)

            # self.screen_handler.present_quit_button()

            # Highlight possible moves if a piece is selected
            if clicked_piece:
                possible_options = self.display_piece_options(clicked_piece)

            # Update the display
            pygame.display.flip()

    # Function that displays on the board the chosen piece's available spaces to move to.
    # Open spaces are displayed in light green.
    def display_piece_options(self, piece):
        response = self.http_handler.check_piece_options(self.game_id, piece.piece_id)
        options = response["piece_options"]
        for option in options:
            self.board.color_square(option, (0, 255, 0))
        return options
