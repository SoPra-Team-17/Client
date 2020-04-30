import logging
import cppyy
from network.Callback import Callback

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("LibClient.hpp")
cppyy.include("util/UUID.hpp")


class LibClientHandler:

    def __init__(self, controller):
        """
        todo bei caro funktioniert das auch ohne diese lokalen variablen, konnte den Grund aber noch nicht finden
        :param controller:
        """
        self.callback = Callback()
        self.make_shared_callback = cppyy.py_make_shared(Callback)
        self.make_shared_model = cppyy.py_make_shared(cppyy.gbl.libclient.Model)
        model = cppyy.gbl.libclient.Model()
        network = cppyy.gbl.libclient.Network(self.make_shared_callback(self.callback), self.make_shared_model(model))
        self.lib_client = cppyy.gbl.libclient.LibClient(self.make_shared_callback(self.callback))

        del network, model

    def connect(self, servername: str, port: int) -> bool:
        if isinstance(servername, str) and isinstance(port, int):
            return self.lib_client.network.connect(servername, port)
        else:
            raise TypeError("Invalid Servername or Port type")

    def disconnect(self) -> bool:
        return self.lib_client.network.disconnect()

    def sendHello(self, name: str, role: cppyy.gbl.spy.network.RoleEnum) -> bool:
        # instance of spy.network.RoleEnum is represented as int!
        if isinstance(name, str) and isinstance(role, int):
            logging.info(f"Send Hello Message: Name: {name} Role: {role}")
            return self.lib_client.network.sendHello(name, role)
        else:
            raise TypeError("Invalid Name or Role type")

    def sendReconnect(self) -> bool:
        return self.lib_client.network.sendReconnect()

    def sendItemChoice(self, choice: (cppyy.gbl.spy.util.UUID, cppyy.gbl.spy.gadget.GadgetEnum)) -> bool:
        if isinstance(choice, (cppyy.gbl.spy.utl.UUID, cppyy.gbl.spy.gadget.GadgetEnum)):
            return self.lib_client.network.sendItemChoice(choice)
        else:
            raise TypeError("Invalid Choice type")

    def sendEquipmentChoice(self, equipMap) -> bool:
        # todo how to handle Map?
        raise Exception("Map handling not implemented")

    def sendGameOperation(self, operation: cppyy.gbl.spy.gameplay.Operation) -> bool:
        if isinstance(operation, cppyy.gbl.spy.gameplay.Operation):
            return self.lib_client.network.sendGameOperation(operation)
        else:
            raise TypeError("Invalid operation type")

    def sendGameLeave(self) -> bool:
        return self.lib_client.network.sendGameLeave

    def sendRequestGamePause(self, gamePause: bool) -> bool:
        if isinstance(gamePause, bool):
            self.lib_client.network.sendRequestGamePause(gamePause)
        else:
            raise TypeError("Invalid gamePause type (not bool)")

    def sendRequestMetaInformation(self, keys) -> bool:
        if isinstance(keys, list) and all(isinstance(elem, str) for elem in keys):
            return self.lib_client.network.sendRequestMetaInformation(keys)
        else:
            raise TypeError("Invalid keys type (not list of strings)")

    def sendRequestReplay(self) -> bool:
        return self.lib_client.network.sendRequestReplay()
