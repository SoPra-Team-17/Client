"""
Implements the actual MainMenu screen
"""
import logging
import json
import pygame_gui.elements.ui_button
import pygame
import cppyy

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/UUID.hpp")
cppyy.include("datatypes/character/PropertyEnum.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")
cppyy.include("datatypes/character/FactionEnum.hpp")
cppyy.include("util/GameLogicUtils.hpp")


class MainMenuScreen(BasicView):
    __connection_dump_path = "assets/Connection/connection.json"

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, parentView,
                 settings: ViewSettings) -> None:
        super(MainMenuScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .375, self.settings.window_height * .4),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager)

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        self.__waiting_for_reconnect = False

        # load title image
        self.titleImage = pygame.image.load("assets/MainMenu/TitleImage.png")
        logging.info("MainMenuScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.titleImage,
                         (self.settings.window_width / 2 - self.titleImage.get_rect().width / 2,
                          self.settings.window_height * .25))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.start_game_button: self.start_game_pressed,
                self.reconnect_button: self.reconnect_pressed,
                self.help_button: self.help_button_pressed,
                self.settings_button: self.settings_button_pressed,
                self.end_game_button: self.controller.exit_game
            }
            switcher.get(event.ui_element)()

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                self._reconnect_game_status()

    def start_game_pressed(self) -> None:
        """
        Start game Button pressed. Connect to server. If successfull go to lobby view
        :return:
        """
        success = self.controller.connect_to_server(self.settings.address, self.settings.port)
        if success:
            self.controller.to_lobby_view()

    def reconnect_pressed(self) -> None:
        """
        Reconnect button pressed. Try to restore old game
        :return:    None
        """
        parsed_json = {}
        try:
            with open(self.__connection_dump_path, "r") as f:
                parsed_json = json.load(f)
        except FileNotFoundError:
            logging.warning("Connection file does not exist")

        ret = False

        try:
            session_cpp = cppyy.gbl.spy.util.UUID(parsed_json["session_id"])
            client_id = cppyy.gbl.spy.util.UUID(parsed_json["client_id"])
            player_one_id = cppyy.gbl.spy.util.UUID(parsed_json["player_one_ide"])
            player_two_id = cppyy.gbl.spy.util.UUID(parsed_json["player_two_id"])
            server_str = parsed_json["server"]
            port = int(parsed_json["port"])
            name = parsed_json["name"]
            player_one_name = parsed_json["player_one_name"]
            player_two_name = parsed_json["player_two_name"]
            self.controller.lib_client_handler.lib_client.reconnectPlayerAfterCrash(server_str, port, name, client_id,
                                                                                    session_cpp, player_one_id,
                                                                                    player_two_id, player_one_name,
                                                                                    player_two_name)
        except KeyError:
            logging.warning("Json file did not contain needed keys")

        if not ret:
            return

        self.__waiting_for_reconnect = True
        logging.info("Successfully reconnected")

    def help_button_pressed(self) -> None:
        """
        Implements transition to help
        :return:    None
        """
        self.parent_view.help_button_pressed()

    def settings_button_pressed(self) -> None:
        """
        Implements transition to settings screen
        :return:    None
        """
        self.parent_view.to_settings()

    def _init_ui_elements(self) -> None:
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.container.get_size()[0] / 2.75, self.__padding * len(self.container.elements)),
                self.__buttonSize),
            text="Start Game",
            manager=self.manager,
            container=self.container
        )

        self.reconnect_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.container.get_size()[0] / 2.75, self.__padding * len(self.container.elements)),
                self.__buttonSize),
            text="Reconnect",
            manager=self.manager,
            container=self.container
        )

        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.get_size()[0] / 2.75,
                                       self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Help",
            manager=self.manager,
            container=self.container
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.get_size()[0] / 2.75,
                                       self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Settings",
            manager=self.manager,
            container=self.container
        )
        self.end_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.get_size()[0] / 2.75,
                                       self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="End Game",
            manager=self.manager,
            container=self.container
        )

    def _reconnect_game_status(self) -> None:
        pass
