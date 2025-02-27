import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the character"""
    
    def __init__(self, op_game):
        """Create a bullet object at the character's current position"""
        # super to inherit properly from Sprite
        super().__init__()
        self.screen = op_game.screen
        self.settings = op_game.settings
        self.colour = self.settings.bullet_colour

        # Create a bullet rect at (0,0) and then set current position.
        self.rect = pygame.Rect(
            0,
            0,
            self.settings.bullet_width,
            self.settings.bullet_height,
            )
        # This will make bullet emerge from the top of the
        # ship to make it look like it's fired from the ship.
        self.rect.midtop = op_game.character.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)    
