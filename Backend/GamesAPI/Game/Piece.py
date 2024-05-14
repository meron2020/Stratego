class Piece:
    def __init__(self, _piece_strength, _color, _name, piece_id, _position=None):
        self.piece_id = piece_id
        self.position = _position
        self._strength = _piece_strength
        self._color = _color
        self._name = _name

    @staticmethod
    def create_piece_from_dict(piece_dict):
        return Piece(piece_dict["_strength"], piece_dict["_color"], piece_dict["_name"], piece_dict["piece_id"],
                     piece_dict["position"])

    # Property method for piece color
    @property
    def color(self):
        return self._color

    # Property method for piece position
    # Property method for piece strength
    @property
    def strength(self):
        return self._strength

    # Property method for name
    @property
    def name(self):
        return self._name

    # Function to update piece position after move
    def set_new_piece_position(self, new_position):
        self.position = new_position
