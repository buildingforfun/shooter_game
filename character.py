import pygame
from pygame.sprite import Sprite

class Character(Sprite):
    """ A class that represents the Character"""

    def __init__(self, op_game):
        """Initialises the character and sets it's original position"""
        super().__init__()
        self.screen = op_game.screen
        self.settings = op_game.settings
        self.screen_rect = op_game.screen.get_rect()

        # Load character image and get its rect
        self.image = pygame.image.load('images/rick.bmp')
        self.rect = self.image.get_rect()

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Start each new character at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def update(self):
        """Update the character's position based on the movement flag."""
        # Update the character's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.character_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.character_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the character at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_character(self):
        """Center the character on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)




