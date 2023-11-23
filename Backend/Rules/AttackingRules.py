from Backend.Piece import Piece


# Class that defines the rules for who wins in attack scenarios.
class AttackingRules:
    # Checks if the result of the battle will be a tie.
    @staticmethod
    def check_tie(attacker: Piece, defender: Piece):
        return attacker.strength == defender.strength

    # Checks different scenarios and determines who wins in each scenario.
    @staticmethod
    def check_battle_winner(attacker: Piece, defender: Piece):
        # If the defender is a bomb, it will win unless the attacker is a Miner.
        if defender.strength == 'B':
            if attacker.strength == 3:
                return attacker
            else:
                return defender

        # If a spy attacks the marshall,the spy wins.
        # Note: This is only the case if the spy is attacking and not vice versa
        elif attacker.strength == 1 and defender.strength == 10:
            return attacker

        # The piece with the higher strength will win.
        elif attacker.strength > defender.strength:
            return attacker

        elif attacker.strength < defender.strength:
            return defender
