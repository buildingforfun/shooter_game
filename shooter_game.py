import sys
import pygame
from time import sleep

# Local imports
from setting import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from character import Character
from bullet import Bullet
from target import Target

class OnePieceShooter:
    """  """

    def __init__(self):
        """ Initialising the game"""
        pygame.init()
        # Make an instance of Settings
        self.settings = Settings()

        # creates window
        self.screen = pygame.display.set_mode((900, 700))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("One Piece Shooter")
        # create objects
        self.character = Character(self)
        self.bullets = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        # Create an instance to store game statistics
        # and create a scoreboard.
        self.sb = Scoreboard(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.character.update()
                self._update_bullets()
                self._update_targets()
            
            self._update_screen()
                

            

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    

    def _check_keydown_events(self, event):                
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
                
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_target_collisions()

    def _check_bullet_target_collisions(self):
        """Respond to bullet-target collisions """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.targets, True, True)
        

        if collisions:
            for target in collisions.values():
                self.stats.score += self.settings.target_points * len(self.targets)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.targets:
            # Destroy existings bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _update_targets(self):
        """Check if fleet at edge and update the position of all targets"""
        self._check_fleet_edges()
        self.targets.update()

        if pygame.sprite.spritecollideany(self.character, self.targets):
            self._character_hit()

        # Look for targets hitting the bottom of the screen
        self._check_targets_bottom()
    
    def _create_target(self,target_no, row_no):
        # Create target and place it in the row
        target = Target(self)
        target_width = target.rect.width
        target.x = target_width + 2 * target_width * target_no
        target.rect.x = target.x
        target.rect.y = target.rect.height + 2 * target.rect.height * row_no
        self.targets.add(target)

    def _create_fleet(self):
        """Create the fleet of targets"""
        # adding instane of target to group that will hold fleet
        number_of_targets = 10
        number_of_rows = 2
        for row_no in range(number_of_rows):
            for target_no in range(number_of_targets):
                self._create_target(target_no, row_no)

    def _check_fleet_edges(self):
        """Respond appropriately if any targets have reached an edge"""
        for target in self.targets.sprites():
            if target.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for target in self.targets.sprites():
            target.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_colour)
        self.character.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.targets.draw(self.screen)

        # Draw the score information
        self.sb.show_score()
        
        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _character_hit(self):
        """Respond to the character being hit by a target"""
        if self.stats.characters_left > 0:
            # Decrement character_left, and update scoreboard
            self.stats.characters_left -= 1
            self.sb.prep_characters()

            # Get rid of remaining targets and bullets
            self.targets.empty()
            self.bullets.empty()

             # Create a new fleet and center the character
            self._create_fleet()
            self.character.center_character()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

     
    def _check_targets_bottom(self):
        """Check if any targets have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for target in self.targets.sprites():
            if target.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if character got hit
               self._character_hit()
               break
    
    def _check_play_button(self, mouse_pos):
        """Starts a new game when player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_characters()

            # Get rid of any remaining targets and bullets
            self.targets.empty()
            self.bullets.empty()

            # Create a new fleet and center the character
            self._create_fleet()
            self.character.center_character()

            # Hide the mouse cursor
            pygame.mouse.set_cursor(False)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    op = OnePieceShooter()
    op.run_game()






