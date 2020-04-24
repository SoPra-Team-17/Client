from network.Callback import Callback


class LibClientHandler:

    def __init__(self):
        self.callback = Callback()

    def init_model(self):
        """
        todo create c++ instance of model --> create LibClient in here
        :return:
        """

    # todo check all types
    # in den folgenden Funktionen müssen die typen auf c++ typen gewandelt werden und Libclient.network aufrufen
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
