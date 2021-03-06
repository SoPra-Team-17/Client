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
    def to_lobby_view(self) -> None:
        """
        Interface to MainMenu View
        :return:    None
        """

    @abstractmethod
    def to_game_view_reconnect(self, target_screen) -> None:
        """
        Interface to GameView when trying to reconnect
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
    def send_reconnect(self) -> bool:
        pass

    @abstractmethod
    def send_item_choice(self, choice) -> bool:
        pass

    @abstractmethod
    def send_equipment_choice(self, equipMap) -> bool:
        pass

    @abstractmethod
    def send_game_operation(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def send_game_leave(self) -> bool:
        pass

    @abstractmethod
    def send_request_game_pause(self, gamePause: bool) -> bool:
        pass

    @abstractmethod
    def send_request_meta_information(self, keys) -> bool:
        pass

    @abstractmethod
    def send_request_replay(self) -> bool:
        pass

    @abstractmethod
    def to_main_menu(self) -> None:
        """
        Interface to GameView
        :return:    None
        """


class ControllerSpectatorView(ABC):
    """
    Specifies interface from spectator view to controller
    """

    @abstractmethod
    def send_request_meta_information(self, keys) -> bool:
        pass

    @abstractmethod
    def send_request_replay(self) -> bool:
        pass

    @abstractmethod
    def to_main_menu(self) -> None:
        """
        Interface to GameView
        :return:    None
        """


class ControllerLobby(ABC):
    """
    Specifies interface from lobby view to controller
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def connect_to_server(self, servername: str, port: int) -> bool:
        """
        Interface to network
        :return:    None
        """

    @abstractmethod
    def disconnect_from_server(self) -> None:
        """
        Interface to network
        :return:    None
        """

    @abstractmethod
    def send_reconnect(self) -> bool:
        """
        Interface to network
        :return:    None
        """

    @abstractmethod
    def send_hello(self, name, role) -> bool:
        """
        Interface to Network
        :return:    None
        """

    @abstractmethod
    def to_main_menu(self) -> None:
        """
        Interface to Lobby
        :return:    None
        """

    @abstractmethod
    def to_game_view(self) -> None:
        """
        Interface to Lobby
        :return:    None
        """

    @abstractmethod
    def selected_spectator_role(self) -> None:
        """
        Interface to Lobby
        :return:    None
        """
