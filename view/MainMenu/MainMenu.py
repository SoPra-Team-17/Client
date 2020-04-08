import logging
import ipaddress
from typing import Dict
import pygame

from view.BasicView import BasicView
from view.MainMenu.MainMenuScreen import MainMenuScreen
from view.MainMenu.SettingsScreen import SettingsScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu


class MainMenu(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, settings: ViewSettings) -> None:
        super(MainMenu, self).__init__(window, controller, settings)

        self.active_screens = []
        self.mainMenuScreen = MainMenuScreen(self.window, self.controller, self, self.settings)
        self.settingsScreen = SettingsScreen(self.window, self.controller, self, settings)

        self.active_screens.append(self.mainMenuScreen)
        logging.info("MainMenu init done")

    def init(self) -> None:
        """
        Not yet implemented
        :return:    None
        """

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.receive_event(event)

    def to_settings(self) -> None:
        self.active_screens = [self.settingsScreen]

    def to_help(self) -> None:
        logging.error("Help Screen not yet implemented")

    def to_main_menu(self, settings: Dict) -> None:
        try:
            width, height = settings["resolution"].split("x")
            width, height = int(width), int(height)
            self.settings.window_height, self.settings.window_width = height, width
        except ValueError:
            logging.warning("Unable to parse Resolution")
        try:
            self.settings.address = ipaddress.ip_address(settings["address"])
        except ValueError:
            logging.warning("Unable to parse IP-Address")
        try:
            self.settings.port = settings["port"]
        except ValueError:
            logging.warning("Unable to parse port")

        self.settings.audio_effects = settings["audio_effects"]
        self.settings.audio_music = settings["audio_music"]

        logging.info(self.settings)

        self.active_screens = [self.mainMenuScreen]
