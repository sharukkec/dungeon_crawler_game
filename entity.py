"""
This is the Entity module.

This module contains common methods for the Enemy and the Player classes
"""
import pygame


class Entity(pygame.sprite.Sprite):
    """
    This is the Entity class.

    This class contains common methods for the Enemy and the Player classes
    """
    def __init__(self, groups):
        """
        This constructor sets up all settings
        """
        super().__init__(groups)
        # init setup
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        """
        This method moves entity's hitbox in dependence with its direction and speed
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        This method checks for vertical and horizontal collisions with obstacle sprites
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
