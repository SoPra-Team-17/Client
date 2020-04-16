import logging
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.HUDScreen import HUDScreen
from controller.ControllerView import ControllerGameView


class HUDView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings) -> None:
        super(HUDView, self).__init__(window, controller, settings)

        self.hudScreen = HUDScreen(window, controller, settings, self)

        self.active_screens = [self.hudScreen]

        logging.info("HUDView init done")

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.receive_event(event)
