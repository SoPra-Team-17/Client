import cppyy
from network.Callback import Callback

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("LibClient.hpp")

class LibClientHandler:

    def __init__(self, controller):
        self.callback = Callback(controller)
        #self.lib_client = cppyy.gbl.libclient.LibClient()
        self.model = cppyy.gbl.libclient.Model()
        self.model.clientState.name = "Das ist ein Name"
        print("Is connected model: ", self.model.clientState.name)

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
