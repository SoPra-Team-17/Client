from abc import ABC

#todo implementation of gadget and subclasses is not ideal, better ideas are welcome

class Gadget(ABC):
    def __init__(self, gadgetRange: int = -1, probability: float = -1.0, damage: int = -1, usagesLeft: int = -1):
        self.range = gadgetRange
        self.probability = probability
        self.damage = damage
        self.usagesLeft = usagesLeft

class HairDryer(Gadget):
    def __init__(self, gadgetRange: int, usagesLeft: int):
        super().__init__(gadgetRange=gadgetRange, usagesLeft=usagesLeft)


class MoleDie(Gadget):
    def __init__(self, gadgetRange: int):
        super().__init__(gadgetRange=gadgetRange)


class TechnicolourPrism(Gadget):
    def __init__(self, gadgetRange: int):
        super().__init__(gadgetRange=gadgetRange)


class BowlerBlade(Gadget):
    """
    does not need __init__ as it is directly derived
    """


        super().__init__()
    def __init__(self):
        super().__init__(-1, -1.0, -1, -1)


class PoisonPills(Gadget):
    def __init__(self):
        super().__init__()


class LaserCompact(Gadget):
    def __init__(self, probability: float):
        super().__init__(probability=probability)


class RocketPen(Gadget):
    def __init__(self, damage: int):
        super().__init__(damage=damage)


class GasGloss(Gadget):
    def __init__(self, gadgetRange: int, damage: int, usagesLeft: int):
        super().__init__(gadgetRange=gadgetRange, damage=damage, usagesLeft=usagesLeft)


class MothballPouch(Gadget):
    def __init__(self, gadgetRange: int, damage: int, usagesLeft: int):
        super().__init__(gadgetRange, -1.0, damage, usagesLeft)


class FogTin(Gadget):
    def __init__(self, gadgetRange: int, usagesLeft: int):
        super().__init__(gadgetRange, -1.0, -1, usagesLeft)


class Grapple(Gadget):
    def __init__(self, gadgetRange: int, probability: float):
        super().__init__(gadgetRange, probability, -1, -1)


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
        super().__init__(usagesLeft=usagesLeft)


class MirrorOfWilderness(Gadget):
    def __init__(self, probability: float, usagesLeft: int):
        super().__init__(probability=probability, usagesLeft=usagesLeft)


class PocketLitter(Gadget):
    def __init__(self):
        super().__init__()


class DiamondCollar(Gadget):
    def __init__(self):
        super().__init__()
