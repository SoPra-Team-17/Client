"""
Implements the screen, shown to the spectator while the choice and equipment phase are in progress
"""
import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerSpectatorView
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "04.06.2020 (creation)"


class SpectatorChoiceScreen(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerSpectatorView, parent_view,
                 settings: ViewSettings) -> None:
        super(SpectatorChoiceScreen, self).__init__(window, controller, settings)

        self.parent = parent_view
        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .35, self.settings.window_height * .4),
                                      (self.settings.window_width / 2, self.settings.window_height / 2)),
            manager=self.manager
        )

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.container.rect.width, self.container.rect.height)),
            text="Item choice and equipment phase in progress. Waiting for the players to be finished...",
            manager=self.manager,
            container=self.container,
            object_id="#info_label"
        )

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        logging.info("Spectator choice screen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                logging.info("Received first game status, going to playing field")
                self.parent.to_playing_field()
