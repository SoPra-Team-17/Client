import pygame

from view.BasicView import BasicView
from view.GameView.GameViewController import GameViewController
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class GameView(BasicView):
    """
    This class implements the interface of the GameView classes to the main controller
    """

    def __init__(self, window: pygame.display, controller: ControllerGameView, setttings: ViewSettings) -> None:
        super().__init__(window, controller, setttings)
        self.gameViewController = GameViewController(self, setttings)

    def draw(self) -> None:
        self.window.fill((50, 50, 50))

        self.gameViewController.draw()

        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        # todo for now all events are forwarded
        # here the filtering between HUD and Game should take place!
        self.gameViewController.receive_event(event)
