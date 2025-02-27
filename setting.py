class Settings:
    """A class to store all settings for One piece shooter

    Benefit: allows us to work with just one settings object any time we need to access an individual setting

    """

    def __init__(self):
        """ Initilise the game's settings."""
        # Screen settings
        self.screen_width = 2000
        self.screen_height = 800
        self.bg_colour = (255, 230, 255)
        self.bullets_allowed = 7

        # Character settings
        self.character_limit = 3
 
        # Bullet settings
        self.bullet_width = 400
        self.bullet_height = 20
        self.bullet_colour = (60, 60, 60)
        
        # Target settings     
        self.fleet_drop_speed = 0.5

        # How quickly the game speeds up
        self.speedup_scale = 0.8

        # Scoring 
        self.target_points = 50
        # How quickly the target point values increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.character_speed = 1
        self.bullet_speed = 3
        self.target_speed = 0.1

        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = -1

    def increase_speed(self):
        """increase speed settings and target point values"""
        self.character_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.character_speed *= self.speedup_scale

        self.target_points = int(self.target_points * self.score_scale)
        print(self.target_points)


