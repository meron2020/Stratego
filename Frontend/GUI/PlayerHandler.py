import pygame


class PlayerHandler:
    def __init__(self, player_id, board, screen):
        self.player_id = player_id
        self.board = board
        self.screen = screen

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
                            self.httpHandler.piece_act(self.game_id, piece.piece_id, move_option)
                            response = self.httpHandler.get_board(self.game_id)
                            self.board.piece_id_matrix = response["board"]
                            return self.create_pieces_sprites_from_get_request(response["pieces_dict"])
                    for sprite in sprite_group:
                        if sprite.piece_id / 100 == self.player_id:
                            if sprite.rect.collidepoint(event.pos):
                                return {"sprite": sprite}
