import pygame
from pygame.sprite import Sprite

class Target(Sprite):
    """A class to represent a singe target in the fleet"""
    
    def __init__(self, op_game):
        """Initialise the target and set its starting position"""
        super().__init__()
        self.screen = op_game.screen
        # create a settings parameter so we can access the target speed in update
        self.settings = op_game.settings

        # Load the target image and set its rect attribute
        self.image = pygame.image.load('images/morty.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new target near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the target's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if target is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or screen_rect.left <= 0:
            return True

    def update(self):
        """Move the target left or right"""
        self.x += self.settings.target_speed
        self.rect.x = self.x

