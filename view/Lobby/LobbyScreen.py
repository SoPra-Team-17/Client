"""
Implements the lobby screen
"""
import logging

import cppyy
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerLobby
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "20.05.20 (doc creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("network/ErrorEnum.hpp")


class LobbyScreen(BasicView):
    _valid_roles = ["Player", "Spectator"]
    _text_labels = {
        "connect": "Connect",
        "name": "Enter name",
        "role": _valid_roles[0],
        "return": "Return"
    }

    def __init__(self, window: pygame.display, controller: ControllerLobby, parentView, settings: ViewSettings) -> None:
        super(LobbyScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .465, self.settings.window_height * .4),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager)

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        logging.info("Lobbyscreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.connect_button: self.connect_pressed,
                self.return_button: self.return_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Did not find UI-Element in Dict")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.controller.to_main_menu()

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "Error":
                self._handle_error()

    def connect_pressed(self) -> None:
        """
        Connect button pressed, extract entered info and send hello to server
        :return:    None
        """
        d = self._extract_info()
        ret = self.controller.send_hello(d["name"], d["role"])
        logging.info(f"Sending Hello successfull: {ret}")

    def return_pressed(self) -> None:
        """
        Return button pressed, send game leave to server
        :return:    None
        """
        ret = self.controller.send_game_leave()
        logging.info(f"Successfully send game leave to server: {ret}")
        self.controller.to_main_menu()

    def _extract_info(self) -> dict:
        """
        Extract information from entryline and dropdown
        :return:
        """
        d = {}
        d["name"] = self.name_entryline.get_text()
        d["role"] = self.role_dropdown.selected_option

        return d

    def _handle_error(self) -> None:
        error_op = self.controller.lib_client_handler.lib_client.getErrorReason()
        if not error_op.has_value():
            return

        desc = None

        if error_op.value() == cppyy.gbl.spy.network.ErrorTypeEnum.NAME_NOT_AVAILABLE:
            desc = "Another Player is already using this name"
        elif error_op.value() == cppyy.gbl.spy.network.ErrorTypeEnum.ALREADY_SERVING:
            desc = "Server is already serving. Maybe connect as a spectator"

        pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((self.settings.window_width * .45, self.settings.window_height * .45),
                             (250, 200)),
            manager=self.manager,
            action_short_name="OK",
            action_long_desc=desc,
            blocking=True
        )

    def _init_ui_elements(self) -> None:
        self.connect_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            text=self._text_labels["connect"],
            manager=self.manager,
            container=self.container,
            object_id="#connect"
        )

        self.name_entryline = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            manager=self.manager,
            container=self.container
        )

        self.role_dropdown = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            options_list=self._valid_roles,
            starting_option=self._text_labels["role"],
            manager=self.manager,
            container=self.container,
            object_id="#role_dropdown"
        )

        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            text=self._text_labels["return"],
            manager=self.manager,
            container=self.container,
            object_id="#return"
        )

        self.name_entryline.set_text(self._text_labels["name"])
