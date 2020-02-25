from abc import ABC, ABCMeta, abstractmethod


class Operation(ABC): pass


class Action(Operation):pass

class Movement(Operation): pass

class Retire(Operation): pass



class GadgetAction(Action): pass
class Roulette(Action): pass
class Cocktails(Action): pass
class Spionieren(Action): pass
class TresorSpicke(Action): pass



