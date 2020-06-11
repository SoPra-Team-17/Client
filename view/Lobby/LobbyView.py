"""
Implements Lobby View
"""
import logging
import json
import pygame

from view.BasicView import BasicView
from view.Lobby.LobbyScreen import LobbyScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerLobby
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "20.05.20 (doc creation)"


class LobbyView(BasicView):
    __connection_dump_path = "assets/Connection/connection.json"

    def __init__(self, window: pygame.display, controller: ControllerLobby, settings: ViewSettings) -> None:
        super(LobbyView, self).__init__(window, controller, settings)

        self.active_screens = []

        self.lobby_screen = LobbyScreen(window, controller, self, settings)

        self.active_screens.append(self.lobby_screen)

        logging.info("Lobby init done")

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        # check for transition to game view
        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "RequestItemChoice":
                logging.info("Go to Item Choice Phase")
                self.dump_connection_info()
                self.controller.to_game_view()

        for screen in self.active_screens:
            screen.receive_event(event)

    def dump_connection_info(self) -> None:
        session_id = self.controller.lib_client_handler.lib_client.getSessionId().to_string_lower()
        player_id = self.controller.lib_client_handler.lib_client.getId().to_string_lower()
        name = self.controller.lib_client_handler.lib_client.getName()
        role = self.controller.lib_client_handler.lib_client.getRole()
        servername = self.settings.address
        port = self.settings.port

        json_dict = {}
        json_dict["session_id"] = session_id
        json_dict["player_id"] = player_id
        json_dict["name"] = name
        json_dict["role"] = role
        json_dict["server"] = servername
        json_dict["port"] = port

        with open(self.__connection_dump_path, "w") as f:
            f.write(json.dumps(json_dict))
