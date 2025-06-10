"""
This is the Enemy module.

This module contains Enemy class and its logic
"""
import pygame
from settings import enemy_data
from entity import Entity
from support import import_folder


class Enemy(Entity):
    """
    This is the Enemy class.

    This class contains enemy's logic
    """
    def __init__(self, enemy_name, pos, groups, obstacle_sprites):
        """
        This is the init contructor method.
        """
        super().__init__(groups)
        self.sprite_type = 'enemy'
        # graphics init
        self.import_graphics(enemy_name)
        self.status = 'right'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_speed = 0.15

        # movement
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = enemy_name
        monster_info = enemy_data[self.monster_name]
        self.max_health = monster_info['health']
        self.health = self.max_health
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack = monster_info['damage']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

    def import_graphics(self, name):
        """
        This method reads all animations for enemy
        """
        enemy_path = f'./images/enemies/{name}/'
        self.animations = {'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [],
                           'attack': [], 'dead': [], 'hurt': []}
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(enemy_path + animation)

    def get_player_distance_direction(self, player):
        """
        This method gets player's and enemy's vectors and evaluate distance and enemy's movement direction
        """
        enemy_vect = pygame.math.Vector2(self.rect.center)
        player_vect = pygame.math.Vector2(player.rect.center)
        distance = (player_vect - enemy_vect).magnitude()
        if distance > 0:
            direction = (player_vect - enemy_vect).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)
        return distance, direction

    def get_status(self, player):
        """
        This method modifies enemy's status depending on distance from player and direction
        """
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]

        if distance <= self.notice_radius:
            if direction.x < 0:
                self.status = 'left'
            else:
                self.status = 'right'
        else:
            # if player is too far, change status to idle
            if not ('idle' in self.status):
                self.status = self.status + '_idle'

    def actions(self, player):
        """
        This method changes enemy's movement direction depending on its status
        """
        if self.status == 'right':
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'left':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2(0, 0)

    def animate(self):
        """
        This method displays animataion
        """
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        """
        This method updates enemy's position and current sprite
        """
        self.move(self.speed)
        self.animate()

    def enemy_upd(self, player):
        """
        This method gets player's position and correct status and actions depending on how close player is
        """
        self.get_status(player)
        self.actions(player)
