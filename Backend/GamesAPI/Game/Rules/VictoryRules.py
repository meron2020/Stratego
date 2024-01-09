class VictoryRules:
    # Function checks if the opposing players flag still exists.
    @staticmethod
    def _check_flag_exists(player_id, pieces_dict):
        if pieces_dict.has_key(player_id * 100 + 1):
            return True
        return False

    # Function checks if the opposing player still has movable pieces.
    @staticmethod
    def _check_has_movable_pieces(player_id, pieces_dict):
        for i in range(2, 38):
            if pieces_dict.has_key(player_id * 100 + i):
                return True
        return False

    # Function takes the player_id of the opposing player and checks if the current player has won.
    # You can win by capturing the enemy flag or destroying all the enemies movable pieces.
    @staticmethod
    def check_player_is_winner(opposing_player, pieces_dict):
        if VictoryRules._check_flag_exists(opposing_player, pieces_dict):
            if VictoryRules._check_has_movable_pieces(opposing_player, pieces_dict):
                return False
            return True
        return True

    @staticmethod
    def check_tie(player, opposing_player, pieces_dict):
        if not VictoryRules._check_has_movable_pieces(player,
                                                      pieces_dict) and not VictoryRules._check_has_movable_pieces(
                opposing_player, pieces_dict):
            return True
        return False
