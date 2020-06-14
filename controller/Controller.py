"""
Implements the Controller, which is the first object created. Handles all interactions between network, user and views
"""
import logging
import sys
import time
import os

import cppyy
import pygame
from cppyy.gbl.std import map, pair, set, vector

from controller.ControllerView import ControllerGameView, ControllerMainMenu, ControllerLobby
from network.LibClientHandler import LibClientHandler
from network.NetworkEvent import NETWORK_EVENT
from view.GameView.GameView import GameView
from view.GameView.SpectatorView import SpectatorView
from view.Lobby.LobbyView import LobbyView
from view.MainMenu.MainMenuView import MainMenuView
from view.ViewSettings import ViewSettings

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("network/RoleEnum.hpp")
cppyy.include("util/UUID.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/gameplay/Movement.hpp")
cppyy.include("datatypes/gameplay/RetireAction.hpp")
cppyy.include("datatypes/gameplay/PropertyAction.hpp")
cppyy.include("datatypes/gameplay/GadgetAction.hpp")
cppyy.include("datatypes/gameplay/SpyAction.hpp")
cppyy.include("datatypes/gameplay/GambleAction.hpp")
cppyy.include("datatypes/character/PropertyEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class Controller(ControllerGameView, ControllerMainMenu, ControllerLobby):
    """
    class implementing a basic controller
    """

    def __init__(self) -> None:
        # call init of ControllerGameView
        super(Controller, self).__init__()
        # call init of ControllerMainMenu
        super(ControllerGameView, self).__init__()

        self.lib_client_handler = LibClientHandler()

        self.view_settings = ViewSettings()

        pygame.init()
        # erstelle screen
        self.screen = pygame.display.set_mode((self.view_settings.window_width, self.view_settings.window_height),
                                              pygame.RESIZABLE)
        pygame.display.set_caption(self.view_settings.window_name)
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenuView(self.screen, self, self.view_settings)
        self.gameView = GameView(self.screen, self, self.view_settings)
        self.lobby_view = LobbyView(self.screen, self, self.view_settings)

        self.active_views = []

        # at the beginning main menu is the active view
        self.active_views.append(self.main_menu)

    def init_components(self) -> None:
        """
        initializes all other components
        Calls init of view
        """
        # initialize components (model,view,self)
        logging.info("Controller init done")

    def loop(self) -> None:
        """
        basic main loop
        :return:    None
        """
        # main game loop is started from here
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                self._handle_critical_network_events(event)
                # distribute events to all active views
                for view in self.active_views:
                    view.receive_event(event)
            # drawing order to all active views
            for view in self.active_views:
                view.draw()

            self.clock.tick(self.view_settings.frame_rate)

    def _handle_critical_network_events(self, event: pygame.event.Event) -> None:
        """
        In this method critical network events, like connection lost are handled
        :return:    None
        """
        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "ConnectionLost":
                logging.warning("Received connection lost event")
                for _ in range(self.view_settings.max_reconnects):
                    success = self.lib_client_handler.sendReconnect()
                    if success:
                        logging.info("Sent reconnect message")
                        return
                    time.sleep(0.05)
                logging.error("Unable to reconnect to server")
                self.lib_client_handler.lib_client.disconnect()
            elif event.message_type == "WrongDestination":
                logging.warning("Received wrong destination event")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VIEW SWITCHES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def to_lobby_view(self) -> None:
        """
        Implements transistion to lobby view. Sets lobbyView as active view
        :return:    None
        """
        logging.info("Active view: lobby view")
        self.active_views = [self.lobby_view]

    def to_game_view(self) -> None:
        """
        Implements transition to game view. Sets gameView as active view and goes directly to item choice screen
        :return:    None
        """
        logging.info("Active view: game view")
        self.active_views = [self.gameView]
        self.gameView.to_item_choice()

        # on transition to game_view request meta information for character names from server
        if isinstance(self.gameView, GameView):
            key_list = [cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
            ret = self.send_request_meta_information(key_list)
            logging.info(f"Send Request Metainformation successfull: {ret}")

    def to_game_view_reconnect(self, target_screen) -> None:
        """
        Implements transition game view when trying to reconnect from the main menu
        :return:    None
        """
        self.gameView.from_reconnect(target_screen)
        self.active_views = [self.gameView]

    def exit_game(self) -> None:
        """
        Exit game button in main menu pressed. Closes window and term. process
        :return:    None
        """
        logging.info("Exit from MainMenu")
        os.remove(self.view_settings.connection_dump_path)
        pygame.quit()
        sys.exit(0)

    def to_main_menu(self) -> None:
        """
        Implements transistion to main menu. Sets mainMenu as active view
        :return:
        """
        self.active_views = [self.main_menu]

    def selected_spectator_role(self) -> None:
        """
        Implements transition to game view, when spectator role is selected
        :return:
        """
        self.gameView = SpectatorView(self.screen, self, self.view_settings)
        self.to_game_view()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SEND NETWORK MESSAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # LobbyView Messages
    def connect_to_server(self, servername: str, port: int) -> bool:
        return self.lib_client_handler.connect(servername, port)

    def disconnect_from_server(self) -> None:
        self.lib_client_handler.disconnect()

    def send_reconnect(self) -> bool:
        return self.lib_client_handler.sendReconnect()

    def send_hello(self, name, role) -> bool:
        # convert String value to c++ enum
        if role == "Player":
            role = cppyy.gbl.spy.network.RoleEnum.PLAYER
        elif role == "Spectator":
            role = cppyy.gbl.spy.network.RoleEnum.SPECTATOR
        else:
            return False

        return self.lib_client_handler.sendHello(name, role)

    # GameView Messages
    def send_item_choice(self, choice) -> bool:
        return self.lib_client_handler.sendItemChoice(choice)

    def send_equipment_choice(self, equipMap) -> bool:
        map_cpp = map[cppyy.gbl.spy.util.UUID, set[cppyy.gbl.spy.gadget.GadgetEnum]]()
        for (char, gad_list) in equipMap.items():
            # for some reason this works and initialization with a list does not
            s = set[cppyy.gbl.spy.gadget.GadgetEnum]()
            for gad in gad_list:
                s.insert(cppyy.gbl.spy.gadget.GadgetEnum(gad))

            p = pair[cppyy.gbl.spy.util.UUID, set[cppyy.gbl.spy.gadget.GadgetEnum]](char, s)
            map_cpp.insert(p)

        return self.lib_client_handler.sendEquipmentChoice(map_cpp)

    def send_game_operation(self, **kwargs) -> bool:
        op_type = kwargs["op_type"]
        try:
            target = kwargs["target"]
        except KeyError:
            target = None

        if target is not None:
            target_cpp = cppyy.gbl.spy.util.Point()
            target_cpp.x = target.x
            target_cpp.y = target.y
            target = target_cpp

        operation = None

        match_config = self.lib_client_handler.lib_client.getSettings()

        active_char_id = self.lib_client_handler.lib_client.getActiveCharacter()
        active_char = self.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            active_char_id)
        if not active_char.getCoordinates().has_value():
            return False

        active_char_coords = active_char.getCoordinates().value()

        if op_type == "Movement":
            operation = cppyy.gbl.spy.gameplay.Movement(False, target, active_char_id, active_char_coords)
        elif op_type == "Retire":
            operation = cppyy.gbl.spy.gameplay.RetireAction(active_char_id)
        elif op_type == "Spy":
            operation = cppyy.gbl.spy.gameplay.SpyAction(active_char_id, target)
        elif op_type == "Gamble":
            stake = kwargs["stake"]
            operation = cppyy.gbl.spy.gameplay.GambleAction(False, target, active_char_id, stake)
        elif op_type == "Property":
            property = kwargs["property"]
            operation = cppyy.gbl.spy.gameplay.PropertyAction(False, target, active_char_id,
                                                              cppyy.gbl.spy.character.PropertyEnum(property))
        elif op_type == "Gadget":
            gadget = kwargs["gadget"]
            gadget_cpp = cppyy.gbl.spy.gadget.GadgetEnum(gadget)
            operation = cppyy.gbl.spy.gameplay.GadgetAction(False, target, active_char_id, gadget_cpp)

        operation = cppyy.gbl.std.make_shared(operation)
        return self.lib_client_handler.sendGameOperation(operation, match_config)

    def send_game_leave(self) -> bool:
        return self.lib_client_handler.sendGameLeave()

    def send_request_game_pause(self, gamePause: bool) -> bool:
        return self.lib_client_handler.sendRequestGamePause(gamePause)

    def send_request_meta_information(self, keys) -> bool:
        keys_cpp = vector[cppyy.gbl.spy.network.messages.MetaInformationKey]()
        for key in keys:
            keys_cpp.push_back(cppyy.gbl.spy.network.messages.MetaInformationKey(key))

        return self.lib_client_handler.sendRequestMetaInformation(keys_cpp)

    def send_request_replay(self) -> bool:
        return self.lib_client_handler.sendRequestReplay()
