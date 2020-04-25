import cppyy

from controller.ControllerNetworkInterface import ControllerNetworkInterface

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.include("Callback.hpp")


class Callback(cppyy.gbl.libclient.Callback):
    """
    Implements a simple callback class which itself calls the controller
    """

    def __init__(self, controller: ControllerNetworkInterface):
        self.controller = controller

    def onHelloReply(self) -> None:
        self.controller.onHelloReply()

    def onGameStarted(self) -> None:
        self.controller.onGameStarted()

    def onRequestChoice(self) -> None:
        self.controller.onRequestChoice()

    def onRequestEquipmentChoice(self) -> None:
        self.controller.onRequestEquipmentChoice()

    def onGameStatus(self) -> None:
        self.controller.onGameStatus()

    def onRequestGameOperation(self) -> None:
        self.controller.onRequestGameOperation()

    def onStatistics(self) -> None:
        self.controller.onStatistics()

    def onGameLeft(self) -> None:
        self.controller.onGameLeft()

    def onGamePause(self) -> None:
        self.controller.onGamePause()

    def onMetaInformation(self) -> None:
        self.controller.onMetaInformation()

    def onStrike(self) -> None:
        self.controller.onStrike()

    def onErrorMessage(self) -> None:
        self.controller.onErrorMessage()

    def onReplay(self) -> None:
        self.controller.onReplay()
