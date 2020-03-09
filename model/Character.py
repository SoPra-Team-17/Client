from model.Scenario import Point


class Character:
    def __init__(self, bp=0, ap=0, hp=100, ip=0):
        self.ID = 0
        self.name = ""
        self.description = ""
        self.Point = None
        self.bp = bp
        self.ap = ap
        self.hp = hp
        self.ip = ip
        self.cocktail = False
        self.chips = 10
        self.properties = []
        self.gadgets = []
