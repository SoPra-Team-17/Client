import cppyy

cppyy.add_include_path("extern/LibClient/src")
cppyy.include("Callback.hpp")


class Callback(cppyy.gbl.libclient.Callback):
    def __init__(self):
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
