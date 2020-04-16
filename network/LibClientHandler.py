import cppyy


class LibClientHandler(cppyy.gbl.CallbackClass):

    def __init__(self):
        pass

    def init_model(self):
        """
        todo create c++ instance of model
        :return:
        """

    # todo check all types
    def sendHello(self, name: str, role):
        pass

    def sendReconnect(self, sessionId):
        pass

    def sendItemChoice(self, chosenCharacterId, chosenGadget):
        pass

    def sendEquipmentChoice(self, equipMap):
        pass

    def sendGameOperation(self, operation):
        pass

    def sendGameLeave(self):
        pass

    def sendRequestGamePause(self, gamePause: bool):
        pass

    def sendMetaInformation(self, keys):
        pass

    def sendRequestReplay(self):
        pass

    def onHelloReply(self):
        pass

    def onGameStarted(self):
        pass

    def onRequestChoice(self):
        pass

    def onRequestEquipmentChoice(self):
        pass

    def onGameStatus(self):
        pass

    def onRequestGameOperation(self):
        pass

    def onStatistics(self):
        pass

    def onGameLeft(self):
        pass

    def onGamePause(self):
        pass

    def onMetaInformation(self):
        pass

    def onStrike(self):
        pass

    def onErrorMessage(self):
        pass

    def onReplay(self):
        pass
