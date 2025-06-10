"""
This is the tile module for the game.

This module contains tile class which places all surrounding tiles
"""
import pygame
from settings import TILESIZE


class Tile(pygame.sprite.Sprite):
    """
    This is the tile class for the game.

    This class places all surrounding tiles
    """
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((64, 64))):
        """
        This constructor sets up all basic setting for this class
        """
        super().__init__(groups)
        # init wall and decoration tiles and scale them
        self.sprite_type = sprite_type
        self.image = surface
        self.scaler()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def scaler(self):
        """
        This method scales tile to fit into TILESIZE
        """
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
