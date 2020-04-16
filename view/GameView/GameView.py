import pygame

from view.BasicView import BasicView
from view.GameView.GameViewController import GameViewController
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class GameView(BasicView):
    """
    This class implements the interface of the GameView classes to the main controller
    """
    def __init__(self, window: pygame.display, controller: ControllerGameView) -> None:
        super().__init__(window, controller)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.active_views = []

        self.gameViewController = GameViewController(self)

        self.active_views.append(self.gameViewController)


    def draw(self) -> None:
        self.window.fill((50, 50, 50))

        for view in self.active_views:
            view.draw()

        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        # todo for now all events are forwarded
        # here the filtering between HUD and Game should take place!
        self.gameViewController.receive_event(event)
