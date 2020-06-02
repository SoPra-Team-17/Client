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


class FloorAssets(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/PolyPixel2D/assets_1024x1024/isometric_0057.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))

        self.hovered_image = self.block_image.copy()
        self.hovered_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.hovered_image.fill((0, 255, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.selected_image = self.block_image.copy()
        self.selected_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.selected_image.fill((255, 255, 0, 0), None, pygame.BLEND_RGBA_ADD)

        self.active_char_image = self.block_image.copy()
        self.active_char_image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.active_char_image.fill((255, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)


class WallAssets(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/PolyPixel2D/assets_1024x1024/isometric_0215.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class FireplaceAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/Lamp.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class RouletteTableAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/PolyPixel2D/assets_1024x1024/isometric_0037.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class BarSeatAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/Chair1.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class BarTableAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/Desk1.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class CharacterAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/PolyPixel2D/assets_1024x1024/isometric_0019.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class GadgetAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/PolyPixel2D/assets_1024x1024/isometric_0048.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class SafeAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/PolyPixel2D/assets_1024x1024/isometric_0153.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class FogAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/PolyPixel2D/assets_1024x1024/isometric_0063.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class JanitorAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/PolyPixel2D/assets_1024x1024/isometric_0018.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class CatAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/PolyPixel2D/assets_1024x1024/isometric_0017.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))

class CocktailAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/GameView/cocktail.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (48, 48))

class AssetStorage():

    def __init__(self):
        self.block_assets = FloorAssets()
        self.wall_assets = WallAssets()
        self.fireplace_assets = FireplaceAsset()
        self.roulettetable_assets = RouletteTableAsset()
        self.barseat_assets = BarSeatAsset()
        self.bartable_assets = BarTableAsset()
        self.character_assets = CharacterAsset()
        self.gadget_assets = GadgetAsset()
        self.safe_assets = SafeAsset()
        self.fog_assets = FogAsset()
        self.janitor_assets = JanitorAsset()
        self.cat_assets = CatAsset()
        self.cocktail_assets = CocktailAsset()
