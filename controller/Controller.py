"""
Implements the Controller, which is the first object created. Handles all interactions between network, user and views
"""
import sys
import logging
import pygame
import cppyy
from cppyy.gbl.std import map

from view.ViewSettings import ViewSettings
from view.MainMenu.MainMenu import MainMenu
from view.GameView.GameView import GameView
from view.Lobby.LobbyView import LobbyView
from controller.ControllerView import ControllerGameView, ControllerMainMenu, ControllerLobby
from network.LibClientHandler import LibClientHandler

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("network/RoleEnum.hpp")

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

        self.lib_client_handler = LibClientHandler(self)

        self.view_settings = ViewSettings()

        pygame.init()
        # erstelle screen
        self.screen = pygame.display.set_mode((self.view_settings.window_width, self.view_settings.window_height),
                                              pygame.RESIZABLE)
        pygame.display.set_caption(self.view_settings.window_name)
        self.clock = pygame.time.Clock()
        self.mainMenu = MainMenu(self.screen, self, self.view_settings)
        self.gameView = GameView(self.screen, self, self.view_settings)
        self.lobbyView = LobbyView(self.screen, self, self.view_settings)

        self.activeViews = []

        # at the beginning main menu is the active view
        self.activeViews.append(self.mainMenu)

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
                for view in self.activeViews:
                    view.receive_event(event)
            # drawing order to all active views
            for view in self.activeViews:
                view.draw()

            self.clock.tick(self.view_settings.frame_rate)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VIEW SWITCHES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def start_game(self) -> None:
        logging.info("Start game detected")
        self.activeViews = [self.lobbyView]

    def to_game_view(self) -> None:
        self.activeViews = [self.gameView]

    def exit_game(self) -> None:
        logging.info("Exit from MainMenu")
        pygame.quit()
        sys.exit(0)

    def to_main_menu(self) -> None:
        self.activeViews = [self.mainMenu]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SEND NETWORK MESSAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # LobbyView Messages
    def connect_to_server(self, servername: str, port: int) -> bool:
        return self.lib_client_handler.connect(servername, port)

    def disconnect_from_server(self) -> None:
        self.lib_client_handler.disconnect()

    def send_reconnect(self) -> bool:
        return self.lib_client_handler.sendReconnect()

    def send_hello(self, name, role) -> bool:
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
        # convert to c++ map (gadgetenum as int)
        map_cpp = map[int, cppyy.gbl.spy.util.UUID]
        for (gad, char) in equipMap.items():
            map[gad] = char
        return self.lib_client_handler.sendEquipmentChoice(map_cpp)

    def send_game_operation(self, operation) -> bool:
        return self.lib_client_handler.sendGameOperation(operation)

    def send_game_leave(self) -> bool:
        return self.lib_client_handler.sendGameLeave()

    def send_request_game_pause(self, gamePause: bool) -> bool:
        return self.lib_client_handler.sendRequestGamePause(gamePause)

    def send_request_meta_information(self, keys) -> bool:
        return self.lib_client_handler.sendRequestMetaInformation(keys)

    def send_request_replay(self) -> bool:
        return self.lib_client_handler.sendRequestReplay()
