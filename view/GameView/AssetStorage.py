from abc import ABC, abstractmethod
import pygame


class DrawableAssets(ABC):
    """
    Class defines a common interface for all Drawables and their assets
    loading of the needed assets and applying transformations to them if needed

    :note   memory usage should not be a priority, but fps are! That means that every possible image which will be
            needed should already be created and stored in memory and not transformed when needed!
    :todo animationen können auch hier gemacht werden
    """

    @abstractmethod
    def get_standard_image(self):
        pass

    @abstractmethod
    def get_hovered_image(self):
        pass


class BlockAssets(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/block.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))

        self.hovered_image = self.block_image.copy()
        self.hovered_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.hovered_image.fill((0, 255, 0, 0), None, pygame.BLEND_RGBA_ADD)

    def get_standard_image(self):
        return self.block_image

    def get_hovered_image(self):
        return self.hovered_image


class AssetStorage():

    def __init__(self):
        self.block_assets = BlockAssets()
