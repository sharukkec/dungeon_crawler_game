"""
This is the support module for the game.

This module contains some methods which are used by most modules
"""
from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
	"""
	This function reads csv file transforms it and returns as a 2d array
	"""
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map, delimiter=',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map


def import_folder(path):
	"""
	This function reads sprites from given path and returns them as a list
	"""
	surface_list = []
	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list


def import_graphics(path, x=64, y=64):
	"""
	This function imports image from given path and scale it using given arguments
	"""
	image_surf = pygame.image.load(path).convert_alpha()
	image_surf = pygame.transform.scale(image_surf, (x, y))
	return image_surf
