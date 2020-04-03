import logging
import pygame

from view.BasicView import BasicView
from view.MainMenu.MainMenuScreen import MainMenuScreen
from controller.ControllerView import ControllerMainMenu


class MainMenu(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerMainMenu) -> None:
        super(MainMenu, self).__init__(window, controller)

        self.active_screens = []
        self.mainMenuScreen = MainMenuScreen(self.window, self.controller)

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
