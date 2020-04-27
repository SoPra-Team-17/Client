import cppyy

from network.NetworkEvent import create_network_event

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.include("Callback.hpp")


class Callback(cppyy.gbl.libclient.Callback):
    """
    Implements a simple callback class which itself calls the controller
    """

    def __init__(self, ):
        pass

    def on_hello_reply(self) -> None:
        create_network_event({"message_type": "HelloReply"})

    def on_game_started(self) -> None:
        create_network_event({"message_type": "GameStarted"})

    def on_request_choice(self) -> None:
        create_network_event({"message_type": "RequestItemChoice"})

    def on_request_equipment_choice(self) -> None:
        create_network_event({"message_type": "RequestEquipmentChoice"})

    def on_game_status(self) -> None:
        create_network_event({"message_type": "GameStatus"})

    def on_request_game_operation(self) -> None:
        create_network_event({"message_type": "RequestGameOperation"})

    def on_statistics(self) -> None:
        create_network_event({"message_type": "Statistics"})

    def on_game_left(self) -> None:
        create_network_event({"message_type": "GameLeft"})

    def on_game_pause(self) -> None:
        create_network_event({"message_type": "GamePause"})

    def on_meta_information(self) -> None:
        create_network_event({"message_type": "MetaInformation"})

    def on_strike(self) -> None:
        create_network_event({"message_type": "Strike"})

    def on_error_message(self) -> None:
        create_network_event({"message_type": "Error"})

    def on_replay(self) -> None:
        create_network_event({"message_type": "Replay"})
