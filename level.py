"""
This is the Level module for the game.

This module displays map and real time exploration.
"""
import pygame
from tile import Tile
from player import Player
from ui import UI
from support import import_csv_layout, import_folder
from enemy import Enemy
from battle import Battle
from settings import TILESIZE


class Level:
    """
    This is the Level module for the game.

    This Class displays map and real time exploration.
    """
    def __init__(self):
        """
        This is the Level constructor which sets up all settings
        """
        # initialization
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.create_map()
        self.ui = UI()
        # battle and game over flags
        self.is_battle = False
        self.game_over = False
        # potion cooldown settings
        self.potion_cooldown_dur = 2000
        self.potion_cooldown_timer = 0

    def create_tiles(self, style, layout, graphics=None):
        """
        This is a support method for create_map method. it sets all tiles and enemies according to their id in array and their position
        """
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    if style == 'walls':
                        surf = graphics['walls'][int(col)]
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'walls', surf)
                    if style == 'decorations':
                        surf = graphics['decorations'][int(col)]
                        Tile((x, y), [self.visible_sprites], 'decorations', surf)
                    if style == 'enemies':
                        if col == '0':
                            Enemy('skeleton', (x, y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites)
                        elif col == '1':
                            Enemy('zombie', (x, y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites)

    def create_map(self):
        """
        This method creates a map and places all sprites on it based on csv tables in layout
        """
        # load csv tables for each layout and transform them into 2d arrays
        layouts = {
            'walls': import_csv_layout('./images/map/_walls.csv'),
            'decorations': import_csv_layout('./images/map/_decorations.csv'),
            'enemies': import_csv_layout('./images/map/_enemies.csv')
        }
        # load all graphics sprites
        graphics = {
            'walls': import_folder('./images/walls'),
            'decorations': import_folder('./images/decorations')
        }
        # place tile for each layout
        for style, layout in layouts.items():
            self.create_tiles(style, layout, graphics)
        # place a player in the left corner room for this dungeon
        self.player = Player((200, 200), [self.visible_sprites, self.player_sprites], self.obstacle_sprites)

    def battle_start(self):
        """
        This method checks if there's a collision between player and any enemy, if yes, than 'is_battle' flag is 'True'
        """
        if self.player_sprites:
            for player_sprite in self.player_sprites:
                collision_spites = pygame.sprite.spritecollide(player_sprite, self.enemy_sprites, True)
                if collision_spites:
                    for target_sprite in collision_spites:
                        self.target = target_sprite
                        self.battle = Battle(self.player, self.target)
                        self.is_battle = True

    def cooldown(self):
        """
        This method sets a cooldown timer for potion usage
        """
        current_time = pygame.time.get_ticks()
        if current_time > self.potion_cooldown_timer:
            self.potion_cooldown_timer = self.potion_cooldown_dur + current_time
            return True
        return False

    def run(self):
        """
        This method draws the game and switches between battle and exploration (depends on 'is_battle' flag)
        """
        keys = pygame.key.get_pressed()
        # use potion if 'space' button is pressed
        if keys[pygame.K_SPACE] and self.cooldown() and self.player.health < self.player.stats['health']:
            self.player.health += 30
            if self.player.health > self.player.stats['health']:
                self.player.health = self.player.stats['health']
            self.player.potions -= 1
        # if game_over flag, go to main and display game_over window
        if self.game_over:
            return False
        if self.is_battle:
            # starts the battle and removes enemy sprite if player wins
            self.is_battle, self.game_over = self.battle.run()
            self.target.kill()
        else:
            # exploration
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.visible_sprites.enemy_upd(self.player)
            self.battle_start()
            self.ui.display(self.player, self.player.potions, 'exploration')
        return True


class YSortCameraGroup(pygame.sprite.Group):
    """
    This class is used to display all sprites depending on their y position so
    """
    def __init__(self):
        """
        This constructor method sets up all settings
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor as a background image
        self.floor_surface = pygame.image.load('./images/tilemap/floor.png').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (512 * 4, 512 * 4))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        """
        This method draws all sprites as sorted by y-axis
        """
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        # draw all sprites as sorted by y-axis
        for sprites in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprites.rect.topleft - self.offset
            self.display_surface.blit(sprites.image, offset_pos)

    def enemy_upd(self, player):
        """
        This method updates enemy actions by passing player as ana argument
        """
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type ==
                         'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_upd(player)
