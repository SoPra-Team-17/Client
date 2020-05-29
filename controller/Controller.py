"""
Implements the Controller, which is the first object created. Handles all interactions between network, user and views
"""
import sys
import logging
import pygame
import cppyy
from cppyy.gbl.std import map, pair, set, vector

from view.ViewSettings import ViewSettings
from view.MainMenu.MainMenuView import MainMenuView
from view.GameView.GameView import GameView
from view.Lobby.LobbyView import LobbyView
from controller.ControllerView import ControllerGameView, ControllerMainMenu, ControllerLobby
from network.LibClientHandler import LibClientHandler
from network.NetworkEvent import NETWORK_EVENT

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
                # distribute events to all active views
                self._check_network_events(event)
                for view in self.active_views:
                    view.receive_event(event)
            # drawing order to all active views
            for view in self.active_views:
                view.draw()

            self.clock.tick(self.view_settings.frame_rate)

    def _check_network_events(self, event):
        meta_message = event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT and event.message_type == "MetaInformation"

        if not meta_message:
            return

        # info is cpp map from MetaInformationKey -> variant(all types)
        info = self.lib_client_handler.lib_client.getInformation()
        logging.info(f"Information: {info}")
        char_information_arr = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        logging.info(f"CharInfo: {char_information_arr}")
        val = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](char_information_arr)
        logging.info(f"Value: {val}")

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
        key_list = [cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        ret = self.send_request_meta_information(key_list)
        logging.info(f"Send Request Metainformation successfull: {ret}")

    def exit_game(self) -> None:
        """
        Exit game button in main menu pressed. Closes window and term. process
        :return:    None
        """
        logging.info("Exit from MainMenu")
        pygame.quit()
        sys.exit(0)

    def to_main_menu(self) -> None:
        """
        Implements transistion to main menu. Sets mainMenu as active view
        :return:
        """
        self.active_views = [self.main_menu]

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

        active_char = self.lib_client_handler.lib_client.getActiveCharacter()
        active_char_coords = self.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            active_char).getCoordinates().value()

        if op_type == "Movement":
            operation = cppyy.gbl.spy.gameplay.Movement(False, target, active_char, active_char_coords)
            logging.info("Movement op will be send to network")
        elif op_type == "Retire":
            operation = cppyy.gbl.spy.gameplay.RetireAction(active_char)
            logging.info("Retire operation will be sond to network")
        elif op_type == "Spy":
            operation = cppyy.gbl.spy.gameplay.SpyAction(active_char, target)
        elif op_type == "Gamble":
            stake = kwargs["stake"]
            operation = cppyy.gbl.spy.gameplay.GambleAction(False, target, active_char, stake)
        elif op_type == "Property":
            property = kwargs["property"]
            # property = 0 --> Observation, property = 1 --> Bang and Burn
            if property == 0:
                operation = cppyy.gbl.spy.gameplay.PropertyAction(False, target, active_char,
                                                                  cppyy.gbl.spy.character.PropertyEnum(15))
            elif property == 1:
                operation = cppyy.gbl.spy.gameplay.PropertyAction(False, target, active_char,
                                                                  cppyy.gbl.spy.character.PropertyEnum(12))
        elif op_type == "Gadget":
            gadget = kwargs["gadget"]
            gadget_cpp = cppyy.gbl.spy.gadget.GadgetEnum(gadget)
            operation = cppyy.gbl.spy.gameplay.GadgetAction(False, target, active_char, gadget_cpp)

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
