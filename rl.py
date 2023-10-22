from ple.games import base
from fighter import *

import base  # Now Python can find the base module

class FighterGame(base.Game):
    def __init__(self, width=1280, height=720):
        base.Game.__init__(self, width, height)

        self.fighter1 = None  # Init your fighter 1 here
        self.fighter2 = None  # Init your fighter 2 here

        # Map actions to methods
        self.action_map = {
            "retreat": self.fighter1.retreat,
            "approach": self.fighter1.approach,
            "jump": self.fighter1.jump_ai,
            "attack": self.fighter1.attack_ai
        }

    def init(self):
        self.score = 0
        # Initialize game specific attributes, reset fighters' states

    def getScore(self):
        # Assuming the score is fighter1's health minus fighter2's health
        return self.fighter1.health - self.fighter2.health

    def game_over(self):
        # Game over when either fighter's health reaches 0
        return self.fighter1.health <= 0 or self.fighter2.health <= 0

    def step(self, dt, action):
        # Perform the action if it's valid
        if action in self.action_map:
            self.action_map[action](self.fighter2)

        # After performing action, update the game state
        # Update the positions, check for collisions etc.
        self.fighter1.combat_behaviour(self.fighter2)
