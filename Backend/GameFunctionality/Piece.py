class Piece:
    def __init__(self, piece_strength, color, name, piece_id):
        self.piece_id = piece_id
        self._position = None
        self._strength = piece_strength
        self._color = color
        self._name = name

    # Property method for piece position
    @property
    def position(self):
        return self._position

    # Property method for piece color
    @property
    def color(self):
        return self._color

    # Property method for piece strength
    @property
    def strength(self):
        return self._strength

    @property
    def name(self):
        return self._name

    # Function to update piece position after move
    def move_piece(self, new_position):
        self._position = new_position
