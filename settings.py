"""
This is the settings module for the game.

This module contains all constant settings which are used in most modules and can be changed in the future
"""
# screen settings
WIDTH = 1400
HEIGTH = 720
FPS = 60
TILESIZE = 64

# UI settings
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
ITEM_BOX_SIZE = 80
FONT = './fonts/Pixeltype.ttf'
FONT_SIZE = 32
LVL_BOX_WIDTH = 48
LVL_BOX_HEIGHT = 28

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BG_COLOR = '#5a5a5a'
UI_BORDER_COLOR = '#111111'

# enemies' statistics
enemy_data = {
    'zombie': {'health': 60, 'damage': 10, 'speed': 2, 'attack_type': 'punch', 'exp': 50, 'notice_radius': 64 * 4},
    'skeleton': {'health': 100, 'damage': 20, 'speed': 5.5, 'attack_type': 'slash', 'exp': 75, 'notice_radius': 64 * 6}}

# battle positioning config
GROUND_LEVEL = 650
PLAYER_POS = 400
ENEMY_POS = 1000
