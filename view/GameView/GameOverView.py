"""
Interface between GameView and GameOverView
"""
import logging
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.GameOverScreen import GameOverScreen
from controller.ControllerView import ControllerGameView

__author__ = "Marco Deuscher"
__date__ = "02.06.2020 (creation)"


class GameOverView(BasicView):
    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings):
        super(GameOverView, self).__init__(window, controller, settings)

        self.parent = parent

        self.game_over_screen = GameOverScreen(window, controller, self, settings)

        self.active_screens = [self.game_over_screen]

        logging.info("Init of GameOverView Done")

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.draw()
