"""
Implements the network callback class for the c++ interface
"""
import logging
import cppyy

from network.NetworkEvent import create_network_event

__author__ = "Marco Deuscher"
__date__ = "20.05.2020 (doc creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.include("Callback.hpp")


class Callback(cppyy.gbl.libclient.Callback):
    """
    Implements a simple callback class which itself calls the controller

    each callback function issues a new network event
    """

    def onHelloReply(self) -> None:
        logging.info("Received Hello Reply")
        create_network_event({"message_type": "HelloReply"})

    def onGameStarted(self) -> None:
        logging.info("Received GameStarted")
        create_network_event({"message_type": "GameStarted"})

    def onRequestItemChoice(self) -> None:
        logging.info("Received Request Item Choice")
        create_network_event({"message_type": "RequestItemChoice"})

    def onRequestEquipmentChoice(self) -> None:
        logging.info("Received Request Equipment Choice")
        create_network_event({"message_type": "RequestEquipmentChoice"})

    def onGameStatus(self) -> None:
        logging.info("Received Game Status")
        create_network_event({"message_type": "GameStatus"})

    def onRequestGameOperation(self) -> None:
        logging.info("Received Request Game Operation")
        create_network_event({"message_type": "RequestGameOperation"})

    def onStatistics(self) -> None:
        logging.info("Received Statistics")
        create_network_event({"message_type": "Statistics"})

    def onGameLeft(self) -> None:
        logging.info("Received Game Left")
        create_network_event({"message_type": "GameLeft"})

    def onGamePause(self) -> None:
        logging.info("Received Game Pause")
        create_network_event({"message_type": "GamePause"})

    def onMetaInformation(self) -> None:
        logging.info("Received Meta Information")
        create_network_event({"message_type": "MetaInformation"})

    def onStrike(self) -> None:
        logging.info("Received Strike")
        create_network_event({"message_type": "Strike"})

    def onError(self) -> None:
        logging.info("Received Error")
        create_network_event({"message_type": "Error"})

    def onReplay(self) -> None:
        logging.info("Received Replay")
        create_network_event({"message_type": "Replay"})

    def connectionLost(self) -> None:
        logging.info("Received Connectin lost")
        # todo create network event and ask user if reconnect should be tried or just try to reconnect

    def wrongDestination(self) -> None:
        logging.info("Received Wrong Destination")
