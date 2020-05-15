"""
Implements a storage class for all assets, so they're only loaded once at runtime and not for each element individually
"""
from abc import ABC, abstractmethod
import pygame

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class DrawableAssets(ABC):
    """
    Class defines a common interface for all Drawables and their assets
    loading of the needed assets and applying transformations to them if needed

    :note   memory usage should not be a priority, but fps are! That means that every possible image which will be
            needed should already be created and stored in memory and not transformed when needed!
    :todo animationen können auch hier gemacht werden
    """


class BlockAssets(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/block.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))

        self.hovered_image = self.block_image.copy()
        self.hovered_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.hovered_image.fill((0, 255, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.selected_image = self.block_image.copy()
        self.selected_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.selected_image.fill((255, 255, 0, 0), None, pygame.BLEND_RGBA_ADD)


class AssetStorage():

    def __init__(self):
        self.block_assets = BlockAssets()
