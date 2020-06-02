"""
Defines interface between GameView and Settings screen of the gameview
"""
import logging
import pygame

from view.BasicView import BasicView
from controller.ControllerView import ControllerGameView
from view.ViewSettings import ViewSettings
from view.GameView.SettingsScreen import SettingsScreen

__author__ = "Marco Deuscher"
__date__ = "02.06.2020 (creation)"


class SettingsView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings):
        super(SettingsView, self).__init__(window, controller, settings)
        self.parent = parent
        self.active_screens = []
        self.settings_screen = SettingsScreen(self.window, self.controller, self, self.settings)

        self.active_screens.append(self.settings_screen)
        logging.info("Gameview settings init done")

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.receive_event(event)
