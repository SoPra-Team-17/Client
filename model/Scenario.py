from abc import ABC
from model import Gadgets


class FieldState(ABC):
    pass


class BarTableField(FieldState):
    pass


class RouletteTableField(FieldState):
    pass


class WallField(FieldState):
    pass


class FreeField(FieldState):
    pass


class BarSeatField(FieldState):
    pass


class SafeField(FieldState):
    pass


class FireplaceField(FieldState):
    pass


class Field:
    def __init__(self) -> None:
        self.fieldState = None
        self.gadget = Gadgets.Gadget(0, 0.0, 0, 0)
        self.character = None

        # could be moved to state itself
        self.isDestroyed = False
        self.chipAmount = 0

        self.safeIndex = 0
        self.isFoggy = False


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Map:
    def __init__(self) -> None:
        # array of Fields, data structure should be changed to map <Point(x,y), Field>
        self.map = {}
