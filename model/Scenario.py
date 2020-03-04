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
    def __init__(self):
        self.fieldState = FieldState()
        self.gadget = Gadgets.Gadget(0, 0.0, 0, 0)
        self.character = None

        self.isDestroyed = False
        self.chipAmount = 0

        self.safeIndex = 0
        self.isFoggy = False


class Map:
    def __init__(self):
        # array of Fields
        self.map = [[]]
