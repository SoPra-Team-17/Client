import logging
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.HUDScreen import HUDScreen
from controller.ControllerView import ControllerGameView


class HUDView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings) -> None:
        super(HUDView, self).__init__(window, controller, settings)

        self.hudScreen = HUDScreen(window, controller, settings, self)

        self.parent = parent

        self.active_screens = [self.hudScreen]

        logging.info("HUDView init done")

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.receive_event(event)

    def filter_event(self, event: pygame.event.Event) -> bool:
        """
        Checks if a given pygame event is for the HUD or for the gameview
        :param event:   pygame event
        :return:        true if for HUD, false if for gameView
        """
        return self.hudScreen.container.rect.collidepoint(pygame.mouse.get_pos())

    def received_strike(self) -> None:
        """
        Interface to game view when a strike was recieved
        :return:    None
        """
        self.hudScreen.strike_display_box.update_textbox()
