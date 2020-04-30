import logging
import pygame

from view.BasicView import BasicView
from view.MainMenu.MainMenuScreen import MainMenuScreen
from view.MainMenu.SettingsScreen import SettingsScreen
from view.MainMenu.HelpScreen import HelpScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu


class MainMenu(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, settings: ViewSettings) -> None:
        super(MainMenu, self).__init__(window, controller, settings)

        self.active_screens = []
        self.mainMenuScreen = MainMenuScreen(self.window, self.controller, self, self.settings)
        self.settingsScreen = SettingsScreen(self.window, self.controller, self, settings)
        self.helpScreen = HelpScreen(self.window, self.controller, self, settings)

        self.active_screens.append(self.mainMenuScreen)
        logging.info("MainMenu init done")

    def init(self) -> None:
        """
        Not yet implemented / needed
        :return:    None
        """

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        """
        Receive Event method called by controller
        :param event:   event
        :return:        None
        """
        for screen in self.active_screens:
            screen.receive_event(event)

    def to_settings(self) -> None:
        """
        Interface from children view to parent
        :return:
        """
        self.active_screens = [self.settingsScreen]

    def help_button_pressed(self) -> None:
        """
        Interface from children view to parent
        :return:
        """
        if self.helpScreen in self.active_screens:
            self.active_screens.remove(self.helpScreen)
        else:
            self.active_screens.append(self.helpScreen)

    def to_main_menu(self) -> None:
        """
        Interface from children view to parent
        :param settings:
        :return:
        """
        self.active_screens = [self.mainMenuScreen]
