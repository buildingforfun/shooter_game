
from pygame.sprite import Group

from character import Character

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, op_game):
        """Initialise scorekeeping attributes"""
        self.op_game = op_game
        self.screen = op_game.screen
        self.screen_rect = op_game.screen.get_rect()
        self.settings = op_game.settings
        self.stats = op_game.stats

        # Font settings for scoring information
        self.text_colour = (30, 30, 30)
        import pygame.font
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_characters()


    def prep_score(self):
        """Turn the score into a rendereed image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(self.stats.score)
        self.score_image = self.font.render(
            score_str,
            True,
            self.text_colour,
            self.settings.bg_colour,
        )

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into an rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str,
            True,
            self.text_colour,
            self.settings.bg_colour,
        )

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str,
            True,
            self.text_colour,
            self.settings.bg_colour
            )
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_characters(self):
        """Show how many characters are left"""
        self.characters = Group()
        for character_no in range(self.stats.characters_left):
            character = Character(self.op_game)
            character.rect.x = character_no * character.rect.width
            character.rect.y = 0.5
            self.characters.add(character)

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.characters.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
