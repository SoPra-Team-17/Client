from abc import ABC, abstractmethod


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
    def sendItemChoice(self, choice) -> bool:
        pass

    @abstractmethod
    def sendEquipmentChoice(self, equipMap) -> bool:
        pass

    @abstractmethod
    def sendGameOperation(self, operation) -> bool:
        pass

    @abstractmethod
    def sendGameLeave(self) -> bool:
        pass

    @abstractmethod
    def sendRequestGamePause(self, gamePause: bool) -> bool:
        pass

    @abstractmethod
    def sendRequestMetaInformation(self, keys) -> bool:
        pass

    @abstractmethod
    def sendRequestReplay(self) -> bool:
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
