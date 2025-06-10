"""
This is the player module for the game.

This module is used to change player's parameters
"""
import pygame
from support import import_folder
from entity import Entity


class Player(Entity):
    """
    This is the player class for the game.

    This class is used to change player's parameters
    """
    def __init__(self, pos, groups, obstacle_sprites):
        """
        This constructor sets up all the initial settings
        """
        super().__init__(groups)
        # init setup
        self.image = pygame.image.load('images/player/right_idle/idle_right.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        # graphics
        self.import_player_assets()
        self.status = 'right'
        self.animation_speed = 0.15

        # movement
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

        # statistics
        self.stats = {'health': 100, 'energy': 100, 'lvl-up': 150}
        self.lvl = 1
        self.attack = 10
        self.health = self.stats['health']
        self.energy = 0
        self.exp = 0
        self.potions = 4

    def import_player_assets(self):
        """
        This method imports all animations for player
        """
        character_path = './images/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'attack': [], 'heavy_attack': [], 'hurt': [], 'dead': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self, battle=False):
        """
        This method gets inputs and change player's status
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            # journalist mode :D
            self.attack = 100
        if keys[pygame.K_e]:
            # masochistic mode D:
            self.health = 1
        if not battle:
            # movement
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.status = 'up'
                self.direction.y = -1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = +1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = +1
                self.status = 'right'
            else:
                self.direction.x = 0

    def get_status(self):
        """
        This method changes player's status to idle if no input given
        """
        if self.direction.x == 0 and self.direction.y == 0:
            if not ('idle' in self.status):
                self.status = self.status + '_idle'

    def animate(self):
        """
        This method shows animation for a certain status
        """
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        """
        This method  updates sprite and position at the moment
        """
        self.input()
        self.move(self.speed)
        self.get_status()
        self.animate()
