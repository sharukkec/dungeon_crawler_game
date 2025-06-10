"""
This is the Battle module.

This module contains battle logic and displays battle scene
"""
import random
import pygame
from ui import UI
from support import import_graphics
from settings import WIDTH, HEIGTH, PLAYER_POS, ENEMY_POS, GROUND_LEVEL


class Battle:
    """
        This class contains all methods for battle logic
    """

    def __init__(self, player, enemy):
        """
        This init constructor gets player and enemy parameters, and setup battle settings
        """
        self.display_surf = pygame.display.get_surface()
        self.bg = import_graphics('./images/battle_bg.webp', WIDTH, HEIGTH)
        self.font = pygame.font.Font('./fonts/Pixeltype.ttf', 45)
        self.player = player
        self.enemy = enemy
        self.ui = UI()
        self.player_turn = True
        self.current_step = 0
        self.current_hurt_step = 0
        self.prev_attack_type = None
        # decrease animation speed, so scaled sprites will move smoother
        self.player.animation_speed = 0.1
        self.enemy.animation_speed = 0.1
        self.battle_end = False

    def render(self):
        """
        This method is used to update entities' animations during the battle
        """
        # change animation sprites
        self.player.animate()
        self.enemy.animate()

    def get_status(self):
        """
        This method is used to get player's inputs  and change his status
        """
        if pygame.mouse.get_pressed()[0] == 1:
            self.player.status = 'attack'
        elif pygame.mouse.get_pressed()[2] == 1 and self.player.energy == 100:
            self.player.status = 'heavy_attack'
        else:
            self.player.status = 'right_idle'

    def get_exp(self):
        """
        This method is used to get experience in the end of the battle and increase level if exp is high enough
        """
        self.player.exp += self.enemy.exp
        if self.player.exp >= self.player.stats['lvl-up']:
            self.player.exp -= self.player.stats['lvl-up']
            self.player.lvl += 1
            self.player.attack += 10

    def attack_modifier(self):
        """
        This method is used to double attack damage for heavy attack and set energy as 0
        """
        if self.prev_attack_type == 'heavy_attack':
            self.player.energy = 0
            return 2
        return 1

    def battle_logic(self):
        """
        This method is used to calculate battle logic
        """
        if self.player_turn:
            if self.player.status in ['attack', 'heavy_attack'] and self.current_step < len(
                    self.player.animations['attack']):
                # show attack animations
                self.render()
                self.current_step = self.current_step + 0.13
                self.prev_attack_type = self.player.status
            else:
                if self.current_step >= 4 and self.current_hurt_step < len(self.enemy.animations['hurt']):
                    # show hurt animations
                    self.enemy.status = 'hurt'
                    self.player.status = 'right_idle'
                    self.render()
                    self.current_hurt_step = self.current_hurt_step + 0.13
                else:
                    if self.current_hurt_step >= 4:
                        if self.player.energy < 100:
                            self.player.energy += 50
                        # heavy attack requires  100 energy and has an attack modification
                        mod = self.attack_modifier()
                        self.enemy.health -= random.randint(self.player.attack * mod * 0.7,
                                                            self.player.attack * mod * 1.3)
                        if self.enemy.health <= 0:
                            # end battle if enemy is dead
                            self.get_exp()
                            self.enemy.animation_speed = 0.15
                            self.player.animation_speed = 0.15
                            self.player.potions += random.randint(0, 1)
                            # is_battle = False and is_game_over = False -> go back to exploration
                            return False, False
                        # set steps to 0
                        self.current_hurt_step = 0
                        self.current_step = 0
                        self.enemy.status = 'attack'
                        self.player_turn = False
                    else:
                        self.enemy.status = 'left_idle'
                        self.get_status()
                        self.render()
        else:
            # same logic but enemy attacks immediately after player
            if self.enemy.status == 'attack' and self.current_step < len(self.enemy.animations['attack']):
                self.render()
                self.current_step = self.current_step + 0.13
            else:
                if self.current_step >= 4 and self.current_hurt_step < len(self.player.animations['hurt']):
                    self.player.status = 'hurt'
                    self.enemy.status = 'left_idle'
                    self.render()
                    self.current_hurt_step = self.current_hurt_step + 0.13
                else:
                    if self.current_hurt_step >= 4:
                        self.player.health -= random.randint(self.enemy.attack * 0.7, self.enemy.attack * 1.3)
                        if self.player.health <= 0:
                            # if player is dead sets is_battle = False and is_game_over = True -> shows gameover screen
                            return False, True
                        self.current_hurt_step = 0
                        self.current_step = 0
                        self.player_turn = True
        return True, False

    def run(self):
        """
        This method is used to display battle
        """
        # display background
        self.display_surf.blit(self.bg, (0, 0))
        is_battle, is_game_over = self.battle_logic()
        # scale the sprites and display them
        player_scaled = pygame.transform.scale(self.player.image,
                                               (self.player.rect.width * 3, self.player.rect.height * 3))
        player_scaled_rect = player_scaled.get_rect(bottomleft=(PLAYER_POS, GROUND_LEVEL))
        enemy_scaled = pygame.transform.scale(self.enemy.image, (self.enemy.rect.width * 3, self.enemy.rect.height * 3))
        enemy_scaled_rect = enemy_scaled.get_rect(bottomleft=(ENEMY_POS, GROUND_LEVEL))
        self.display_surf.blit(player_scaled, player_scaled_rect)
        self.display_surf.blit(enemy_scaled, enemy_scaled_rect)
        # display UI
        self.ui.display(self.player, self.player.potions, 'battle', self.enemy)
        # is_battle = True, is_game_over = False -> battle continues!
        return is_battle, is_game_over
