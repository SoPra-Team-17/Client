import pygame

from view.BasicView import BasicView
from view.GameView.GameViewController import GameViewController
from view.GameView.HUDView import HUDView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class GameView(BasicView):
    """
    This class implements the interface of the GameView classes to the main controller
    """

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings) -> None:
        super().__init__(window, controller, settings)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.gameViewController = GameViewController(self, settings)
        self.hudView = HUDView(self.window, self.controller, self.settings)

        self.active_views = [self.gameViewController, self.hudView]

    def draw(self) -> None:
        self.window.fill((50, 50, 50))

        for view in self.active_views:
            view.draw()

        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        # todo for now all events are forwarded
        # here the filtering between HUD and Game should take place!
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.controller.to_main_menu()

        for view in self.active_views:
            view.receive_event(event)
