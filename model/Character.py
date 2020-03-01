from abc import ABC, ABCMeta, abstractmethod


class Character(ABC):
    @abstractmethod
    def __init__(self, bp=0, ap=0, hp=100, ip=0):
        self.ID = 0
        self.name = ""
        self.description = ""
        self.x = 0
        self.y = 0
        self.bp = bp
        self.ap = ap
        self.hp = hp
        self.ip = ip
        self.cocktail = False
        self.chips = 10
        self.properties = []
        self.gadgets = []
