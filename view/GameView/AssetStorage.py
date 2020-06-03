"""
Implements a storage class for all assets, so they're only loaded once at runtime and not for each element individually
"""
from abc import ABC, abstractmethod
import pygame

from assets.GameView.CharactersIso.CharacterIsoPaths import CHARACTER_ISO_PATH_DICT

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
        self.block_image = pygame.image.load(
            "assets/GameView/IsoAssets/PNG/Platformertiles/platformerTile_11.png").convert_alpha()
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
        self.block_image = pygame.image.load(
            "assets/GameView/IsoAssets/PNG/VoxelTiles/voxelTile_30.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class FireplaceAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/GameView/IsoAssets/PNG/VoxelTiles/voxelTile_17.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class RouletteTableAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/GameView/IsoAssets/PNG/VoxelTiles/voxelTile_18.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class BarSeatAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/Chair1.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class BarTableAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load("assets/GameView/Desk1.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class CharacterImages:
    """
    Small dataclass to store character iso images
    """

    def __init__(self, top, bottom, top_active, bottom_active):
        self.top = top
        self.bottom = bottom
        self.active_top = top_active
        self.active_bottom = bottom_active


class CharacterAsset(DrawableAssets):
    def __init__(self):
        self.asset_dict = {}
        for key, val in CHARACTER_ISO_PATH_DICT.items():
            top = pygame.image.load(f"{CHARACTER_ISO_PATH_DICT[key]}/{key}_top.png")
            top = pygame.transform.scale(top, (64, 64))

            bottom = pygame.image.load(f"{CHARACTER_ISO_PATH_DICT[key]}/{key}_bottom.png")
            bottom = pygame.transform.scale(bottom, (64, 64))

            active_top = pygame.image.load(f"{CHARACTER_ISO_PATH_DICT[key]}/{key}_active_top.png")
            active_top = pygame.transform.scale(active_top, (64, 64))

            active_bottom = pygame.image.load(f"{CHARACTER_ISO_PATH_DICT[key]}/{key}_active_bottom.png")
            active_bottom = pygame.transform.scale(active_bottom, (64, 64))

            self.asset_dict[key] = CharacterImages(top, bottom, active_top, active_bottom)


class GadgetAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/GameView/IsoAssets/PNG/Platformertiles/platformerTile_23.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class SafeAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/GameView/IsoAssets/PNG/Platformertiles/platformerTile_40.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class FogAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/PolyPixel2D/assets_1024x1024/isometric_0063.png").convert_alpha()
        self.block_image = pygame.transform.scale(self.block_image, (64, 64))


class CatAsset(DrawableAssets):
    def __init__(self):
        self.block_image = pygame.image.load(
            "assets/GameView/cat.png").convert_alpha()
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
        self.cat_assets = CatAsset()
        self.cocktail_assets = CocktailAsset()
