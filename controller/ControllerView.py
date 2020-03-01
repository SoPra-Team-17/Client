from abc import ABC, abstractmethod
import pygame


class ControllerMainMenu(ABC):
    """
    Specifies interface from main menu to controller
    """

    def __init__(self):
        pass

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def exit_game(self):
        pass


class ControllerGameView(ABC):
    """
    Specifies interface from game view to controller
    """

    def __init__(self):
        pass

    @abstractmethod
    def send_action(self):
        pass
