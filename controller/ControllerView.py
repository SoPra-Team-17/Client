"""
Defines abstract interfaces between views and the controller
"""
from abc import ABC, abstractmethod

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class ControllerMainMenu(ABC):
    """
    Specifies interface from main menu to controller
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def start_game(self) -> None:
        """
        Interface to MainMenu View
        :return:    None
        """

    @abstractmethod
    def exit_game(self) -> None:
        """
        Interface to MainMenu View
        :return:    None
        """


class ControllerGameView(ABC):
    """
    Specifies interface from game view to controller
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def send_action(self) -> None:
        """
        Interface to GameView
        :return:    None
        """

    def to_main_menu(self) -> None:
        """
        Interface to GameView
        :return:    None
        """
