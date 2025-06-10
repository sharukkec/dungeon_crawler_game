"""
This is the menu module for the game.

This module displays main menu screen
"""
import sys
import pygame
from settings import WIDTH


class MainMenu:
    """
    This is the menu class for the game.

    This class displays main menu screen
    """
    def __init__(self):
        """
        This constructor method sets up all fonts and rectangles
        """
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # setup all graphics
        self.title_font = pygame.font.Font('./fonts/Pixeltype.ttf', 70)
        self.font = pygame.font.Font('./fonts/Pixeltype.ttf', 45)
        self.title_text = self.title_font.render("Welcome to Dungeons of Apatity", True, pygame.Color("white"))
        self.title_text_rect = self.title_text.get_rect(center=(WIDTH // 2, 150))
        self.start_text = self.font.render("Start game", True, pygame.Color("white"))
        self.start_text_rect = self.start_text.get_rect(center=(WIDTH // 2, 400))
        self.quit_text = self.font.render("Quit game", True, pygame.Color("white"))
        self.quit_text_rect = self.quit_text.get_rect(center=(WIDTH // 2, 450))
        self.background = pygame.image.load('menu/background2.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, 700))

    def run(self):
        """
        This method displays the menu screen and lets player quit the game or start it
        """
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # show background
        self.display_surface.blit(self.background, (0, 0))
        # show title text
        pygame.draw.rect(self.display_surface, 'Black', self.title_text_rect, 0, 3)
        self.display_surface.blit(self.title_text, self.title_text_rect)
        # show quit_game and start_game buttons, if there's a collision between mouse position and button rectangle,
        # change this rectangle's color. If user clicks on this rectangle, start or quit game
        if self.start_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.display_surface, (90, 90, 90), self.start_text_rect, 0, 3)
            if pygame.mouse.get_pressed()[0] == 1:
                return False

        else:
            pygame.draw.rect(self.display_surface, 'Black', self.start_text_rect, 0, 3)
        self.display_surface.blit(self.start_text, self.start_text_rect)
        if self.quit_text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.display_surface, (90, 90, 90), self.quit_text_rect, 0, 3)
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(self.display_surface, 'Black', self.quit_text_rect, 0, 3)
        self.display_surface.blit(self.quit_text, self.quit_text_rect)

        return True
