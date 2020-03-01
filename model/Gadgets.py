from abc import ABC, ABCMeta, abstractmethod


class Gadget(ABC):
    def __init__(self, range: int, probability: float, damage: int, usagesLeft: int):
        self.range = range
        self.probability = probability
        self.damage = damage
        self.usagesLeft = usagesLeft


class HairDryer(Gadget):
    def __init__(self, range: int, usagesLeft: int):
        super().__init__(range, -1.0, -1, usagesLeft)


class MoleDie(Gadget):
    def __init__(self, range: int):
        super().__init__(range, -1.0, -1, -1)


class TechnicolourPrism(Gadget):
    def __init__(self, range: int):
        super().__init__(range, -1.0, -1, -1)


class BowlerBlade(Gadget):
    def __init__(self, range: int, probability: float, damage: int, usagesLeft: int):
        super().__init__(range, probability, damage, usagesLeft)


class MagneticWatch(Gadget):
    def __init__(self):
        super().__init__(-1, -1.0, -1, -1)


class PoisonPills(Gadget):
    def __init__(self):
        super().__init__(-1, -1.0, -1, -1)


class LaserCompact(Gadget):
    def __init__(self, probability: float):
        super().__init__(-1, probability, -1, -1)


class RocketPen(Gadget):
    def __init__(self, damage: int):
        super().__init__(-1, -1.0, damage, -1)


class GasGloss(Gadget):
    def __init__(self, range: int, damage: int, usagesLeft: int):
        super().__init__(range, -1.0, damage, usagesLeft)


class MothballPouch(Gadget):
    def __init__(self, range: int, damage: int, usagesLeft: int):
        super().__init__(range, -1.0, damage, usagesLeft)


class FogTin(Gadget):
    def __init__(self, range: int, usagesLeft: int):
        super().__init__(range, -1.0, -1, usagesLeft)


class Grapple(Gadget):
    def __init__(self, range: int, probability: float):
        super().__init__(range, probability, -1, -1)


class Jetpack(Gadget):
    def __init__(self, usagesLeft: int):
        super().__init__(-1, -1.0, -1, usagesLeft)


class WiretapWithEarplugs(Gadget):
    def __init__(self, probability: float):
        super().__init__(-1, probability, -1, -1)


class ChickenFeed(Gadget):
    def __init__(self, usagesLeft: int):
        super().__init__(-1, -1.0, -1, usagesLeft)


class Nugget(Gadget):
    def __init__(self, usagesLeft: int):
        super().__init__(-1, -1.0, -1, usagesLeft)


class MirrorOfWilderness(Gadget):
    def __init__(self, probability: float, usagesLeft: int):
        super().__init__(-1, probability, -1, usagesLeft)


class PocketLitter(Gadget):
    def __init__(self):
        super().__init__(-1, -1.0, -1, -1)


class DiamondCollar(Gadget):
    def __init__(self):
        super().__init__(-1, -1.0, -1, -1)
