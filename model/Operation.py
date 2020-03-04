from abc import ABC


class Operation(ABC):
    pass


class Action(Operation):
    pass


class Movement(Operation):
    pass


class Retire(Operation):
    pass


class GadgetAction(Action):
    pass


class GambleAction(Action):
    pass


class SpyAction(Action):
    pass


class Property(Action):
    pass
