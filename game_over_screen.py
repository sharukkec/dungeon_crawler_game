"""
This is the game over module.

This module is used to display game over screen
"""
import pygame
from settings import FONT, FONT_SIZE, WIDTH, HEIGTH


class GameOver:
    """
    This is the game over Class.

    This class is used to display game over screen
    """
    def __init__(self):
        """
        This constructor method is used to set up all settings
        """
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.game_over = self.font.render("Game over !", True, pygame.Color("white"))
        self.game_over_rect = self.game_over.get_rect(center=(WIDTH / 2, HEIGTH / 2))

    def run(self):
        """
        This method displays 'game_over' text
        """
        self.display_surf.blit(self.game_over, self.game_over_rect)
