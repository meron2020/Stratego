import pygame
from Frontend.GUI.Board import Board


class PlayerHandler:
    def __init__(self, player_id, board, screen, http_handler, game_id):
        self.player_id = player_id
        self.board = board
        self.screen = screen
        self.httpHandler = http_handler
        self.game_id = game_id

    def player_set_pieces(self, sprite_group):
        clicked_sprite = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any sprite is clicked
                    for sprite in sprite_group:
                        if sprite.rect.collidepoint(event.pos):
                            clicked_sprite = sprite
                            clicked_sprite.start_drag(event.pos)

                    finish_button_rect = pygame.Rect(
                        pygame.display.get_window_size()[0] - 300,
                        pygame.display.get_window_size()[1] - 150,
                        175, 50
                    )
                    if finish_button_rect.collidepoint(event.pos):
                        return

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

            # Check if bottom four rows are filled
            if self.board.setup_rows_filled(1):
                # Display "Finish set up" button in the bottom right corner
                finish_button_rect = pygame.Rect(
                    pygame.display.get_window_size()[0] - 300,
                    pygame.display.get_window_size()[1] - 150,
                    175, 50
                )

                pygame.draw.rect(self.screen, (0, 0, 255), finish_button_rect)
                font = pygame.font.Font(None, 36)
                text = font.render("Finish set up", True, (255, 255, 255))
                self.screen.blit(text, finish_button_rect.move(10, 5))
                pygame.display.flip()
                # sprite.drag(pygame.mouse.get_pos())
            self.screen.fill((255, 255, 255))

            # Draw the board and pieces
            self.board.draw_board()
            sprite_group.draw(self.screen)

            # Update the display
            pygame.display.flip()

    def user_act(self, sprite_group):
        running = True
        possible_options = None
        clicked_piece = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    selected_square = self.board.get_clicked_square(
                        event.pos)  # Implement this method to get the square position
                    if not possible_options:
                        clicked_piece = Board.get_clicked_sprite_and_position(self.sprite_group, event.pos)
                    else:
                        if selected_square in possible_options:
                            return selected_square
                            # self.httpHandler.piece_act(self.game_id, clicked_piece.piece_id, selected_square)
                            # response = self.httpHandler.get_board(self.game_id)
                            # self.board.piece_id_matrix = response["board"]
                            # self.sprite_group = self.create_pieces_sprites_from_get_request(response["pieces_dict"])
                        else:
                            clicked_piece = Board.get_clicked_sprite_and_position(self.sprite_group, event.pos)

            self.screen.fill((255, 255, 255))
            self.board.draw_board()

            # Draw the pieces
            sprite_group.draw(self.screen)

            # Highlight possible moves if a piece is selected
            if clicked_piece:
                possible_options = self.display_piece_options(clicked_piece)

            pygame.display.flip()

    def display_piece_options(self, piece):
        response = self.httpHandler.check_piece_options(self.game_id, piece.piece_id)
        options = response["piece_options"]
        for option in options:
            self.board.color_square(option, (0, 255, 0))
        return options

    def get_user_piece_act(self, options, sprite_group, piece):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for move_option in options:
                        rect = self.board.create_square_by_row_and_column(move_option[0], move_option[1])
                        if rect.collidepoint(event.pos):
                            return move_option
                    for sprite in sprite_group:
                        if sprite.piece_id / 100 == self.player_id:
                            if sprite.rect.collidepoint(event.pos):
                                return {"sprite": sprite}
