from abc import ABC, abstractmethod


class ControllerNetworkInterface(ABC):
    """
    This class defines the Interface between Network and Controller
    For now it's the same as Callback, but will most likely be narrrowed down /
    more abstracted from the actual received message
    """

    def __init__(self):
        pass

    @abstractmethod
    def onHelloReply(self) -> None:
        pass

    @abstractmethod
    def onGameStarted(self) -> None:
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
