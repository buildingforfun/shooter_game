class GameStats:
    """Track statistics for One Piece shooter"""

    def __init__(self, op_game):
        """Initialise stats"""
        self.settings = op_game.settings
        self.reset_stats()
        
        # Start One Piece in inactive state
        self.game_active = False

        # High score should never be reset
        self.high_score = 0


    def reset_stats(self):
        """Initialise stats that can change during the game"""
        self.characters_left = self.settings.character_limit
        self.score = 0
        self.level = 1