"""
This is the main module for the game.

This module run all other models and update screen.
"""
import sys
import pygame
from settings import WIDTH, HEIGTH, FPS
import menu
from level import Level
from game_over_screen import GameOver


class Game:
    """
    This class is used to show the screen an update information showed on it
    """
    def __init__(self):
        """
        This constructor (__init__) method is used to setup basic settings and flags
        """
        pygame.init()
        # basic settings
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Dungeons of Apatity')
        self.clock = pygame.time.Clock()
        self.menu = menu.MainMenu()
        self.is_menu = True
        self.level = Level()
        self.is_running = True
        self.game_over = GameOver()

    def run(self):
        """
        This method is updating the display and calling methods if certain conditions are met
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.is_menu:
                # if False then runs level on next  frame, otherwise runs menu again
                self.is_menu = self.menu.run()
            elif self.is_running:
                self.screen.fill('#25131A')
                self.is_running = self.level.run()
            else:
                self.screen.fill('#25131A')
                self.game_over.run()
            pygame.display.update()
            # update the display with FPS - equal frequency
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
