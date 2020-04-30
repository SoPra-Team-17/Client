import pygame

from view.BasicView import BasicView
from view.GameView.GameViewController import GameViewController
from view.GameView.HUDView import HUDView
from view.GameView.ItemChoiceScreen import ItemChoiceScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class GameView(BasicView):
    """
    This class implements the interface of the GameView classes to the main controller
    """

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings) -> None:
        super().__init__(window, controller, settings)

        self.game_view_controller = GameViewController(self, settings)
        self.hud_view = HUDView(self.window, self.controller, self.settings)
        self.item_choice_screen = ItemChoiceScreen(self.window, self.controller, self, self.settings)

        self.active_views = [self.item_choice_screen]

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

        if event.type == pygame.MOUSEBUTTONUP and self.hud_view.filter_event(event):
            self.hud_view.receive_event(event)
            return

        for view in self.active_views:
            view.receive_event(event)

    def to_playing_field(self) -> None:
        self.active_views = [self.game_view_controller, self.hud_view]

    def to_item_choice(self) -> None:
        self.active_views = [self.item_choice_screen]
