"""Class for each player object."""

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.position = None
        self.hand = [] 
        self.eliminated = False