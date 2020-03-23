from model.Scenario import Point


class Character:
    def __init__(self, bp: int = 0, ap: int = 0, hp: int = 100, ip: int = 0) -> None:
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
