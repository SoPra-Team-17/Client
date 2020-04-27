"""
This module defines the interfaces between the network and a view
"""
from abc import ABC, abstractmethod

__author__ = "Marco Deuscher"
__date__ = "27.04.2020 (creation)"


class LobbyViewNetwork(ABC):
    """
    This class implement the Interface between the network and the lobby view
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def onHelloReplay(self) -> None:
        pass

    @abstractmethod
    def onErrorMessage(self) -> None:
        pass


class GameViewNetwork(ABC):
    """
    This class implements the interface between the network and the game view
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def onRequestChoice(self) -> None:
        pass

    @abstractmethod
    def onRequestEquipmentChoice(self) -> None:
        pass

    @abstractmethod
    def onGameStatus(self) -> None:
        pass

    @abstractmethod
    def onRequestGameOperation(self) -> None:
        pass

    @abstractmethod
    def onStatistics(self) -> None:
        pass

    @abstractmethod
    def onGameLeft(self) -> None:
        pass

    @abstractmethod
    def onGamePause(self) -> None:
        pass

    @abstractmethod
    def onMetaInformation(self) -> None:
        pass

    @abstractmethod
    def onStrike(self) -> None:
        pass

    @abstractmethod
    def onErrorMessage(self) -> None:
        pass

    @abstractmethod
    def onReplay(self) -> None:
        pass
