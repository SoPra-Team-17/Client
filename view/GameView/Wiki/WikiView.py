"""
BasicView Interface for wiki
"""

import pygame

from view.ViewSettings import ViewSettings
from view.BasicView import BasicView
from view.GameView.Wiki.WikiScreen import WikiScreen
from controller.ControllerView import ControllerGameView

__author__ = "Marco Deuscher"
__date__ = "10.06.2020"


class WikiView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings) -> None:
        super(WikiView, self).__init__(window, controller, settings)

        self.parent = parent

        self.wiki_screen = WikiScreen(self.window, self.controller, self, self.settings)

        self.active_screens = [self.wiki_screen]

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.receive_event(event)
