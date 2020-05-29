"""
Implements interface to LibClient lib
"""
import logging
import cppyy
from network.Callback import Callback

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("LibClient.hpp")
cppyy.include("util/UUID.hpp")
cppyy.include("datatypes/gameplay/BaseOperation.hpp")

__author__ = "Marco Deuscher"
__date__ = "20.05.2020 (doc creation)"


class LibClientHandler:
    """
    Implements a wrapper for the LibClient Object provided by LibClient lib (c++ Lib)
    """

    def __init__(self):
        self.callback = Callback()
        # new make_shared syntax introduced by cppyy==1.7.0
        self.lib_client = cppyy.gbl.libclient.LibClient(self.callback)

    def connect(self, servername: str, port: int) -> bool:
        if isinstance(servername, str) and isinstance(port, int):
            return self.lib_client.network.connect(servername, port)
        else:
            raise TypeError("Invalid Servername or Port type")

    def disconnect(self) -> None:
        self.lib_client.network.disconnect()

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
        if isinstance(choice, int):
            # convert to gadget type!
            return self.lib_client.network.sendItemChoice(cppyy.gbl.spy.gadget.GadgetEnum(choice))
        elif isinstance(choice, (cppyy.gbl.spy.util.UUID)):
            return self.lib_client.network.sendItemChoice(choice)
        else:
            raise TypeError("Invalid Choice type")

    def sendEquipmentChoice(self, equipMap: dict) -> bool:
        return self.lib_client.network.sendEquipmentChoice(equipMap)

    # networks expects shared ptr
    def sendGameOperation(self, operation: cppyy.gbl.spy.gameplay.BaseOperation) -> bool:
        if isinstance(operation, cppyy.gbl.spy.gameplay.BaseOperation):
            return self.lib_client.network.sendGameOperation(operation)
        else:
            raise TypeError("Invalid operation type")

    def sendGameLeave(self) -> bool:
        return self.lib_client.network.sendGameLeave

    def sendRequestGamePause(self, gamePause: bool) -> bool:
        if isinstance(gamePause, bool):
            return self.lib_client.network.sendRequestGamePause(gamePause)
        else:
            raise TypeError("Invalid gamePause type (not bool)")

    def sendRequestMetaInformation(self, keys) -> bool:
        if isinstance(keys, list) and all(isinstance(elem, str) for elem in keys):
            return self.lib_client.network.sendRequestMetaInformation(keys)
        else:
            raise TypeError("Invalid keys type (not list of strings)")

    def sendRequestReplay(self) -> bool:
        return self.lib_client.network.sendRequestReplay()
