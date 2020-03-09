from abc import ABC, abstractmethod


class ControllerMainMenu(ABC):
    """
    Specifies interface from main menu to controller
    """

    def __init__(self):
        pass

    @abstractmethod
    def start_game(self):
        """
        Interface to MainMenu View
        :return:    None
        """

    @abstractmethod
    def exit_game(self):
        """
        Interface to MainMenu View
        :return:    None
        """


class ControllerGameView(ABC):
    """
    Specifies interface from game view to controller
    """

    def __init__(self):
        pass

    @abstractmethod
    def send_action(self):
        """
        Interface to GameView
        :return:    None
        """
