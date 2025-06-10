"""
This is the UI module for the game.

This module contains UI class
"""
import pygame
from settings import *
from support import import_graphics


class UI:
    """
    This is the UI class for the game.

    This class contains UI class
    """
    def __init__(self):
        """
        This constructor sets up all initial settings
        """
        # init setup
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)

        # bars
        self.health_bar_rect = pygame.Rect(10, HEIGTH - 40, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, HEIGTH - 20, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        """
        This method shows health/energy bar
        """
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surf, color, current_rect)
        pygame.draw.rect(self.display_surf, UI_BORDER_COLOR, bg_rect, 3)

    def show_lvl(self, lvl, exp):
        """
        This method shows lvl and exp the player has
        """
        bg_lvl_rect = pygame.Rect(13, HEIGTH - 70, LVL_BOX_WIDTH, LVL_BOX_HEIGHT)
        bg_exp_rect = pygame.Rect(13, HEIGTH - 100, LVL_BOX_WIDTH + 40, LVL_BOX_HEIGHT)

        lvl = self.font.render(f"lvl {lvl}", True, pygame.Color("white"))
        exp = self.font.render(f"{exp}/150", True, pygame.Color("white"))
        lvl_rect = lvl.get_rect(topleft=(18, HEIGTH - 65))
        exp_rect = exp.get_rect(topleft=(18, HEIGTH - 95))
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_lvl_rect)
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_exp_rect)
        self.display_surf.blit(lvl, lvl_rect)
        self.display_surf.blit(exp, exp_rect)

    def potion_box(self, potion_num):
        """
        This method shows potion box and number of potions player has
        """
        bg_potion_rect = pygame.Rect(WIDTH - 90, HEIGTH - 90, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_potion_rect)
        potion = import_graphics('./images/potion.png', ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        potion_num = self.font.render(f"{potion_num}", True, pygame.Color("white"))
        self.display_surf.blit(potion, bg_potion_rect)
        self.display_surf.blit(potion_num, bg_potion_rect.topleft)

    def display(self, player, potion_num, state='exploration', enemy=None):
        """
        This method displays UI with given parameters
        """
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_lvl(player.lvl, player.exp)
        self.potion_box(potion_num)
        if state == 'battle':
            # show enemy's healthbar
            enemy_health_bar_rect = pygame.Rect(ENEMY_POS - 80, GROUND_LEVEL - 300, HEALTH_BAR_WIDTH, BAR_HEIGHT)
            self.show_bar(enemy.health, enemy.max_health, enemy_health_bar_rect, HEALTH_COLOR)
