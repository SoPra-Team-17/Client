"""
Implements game over screen in which the winner and statistics are displayed
"""
import logging
import pygame
import pygame_gui

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView

__author__ = "Marco Deuscher"
__date__ = "02.06.2020 (creation)"


class GameOverScreen(BasicView):
    _victory_enum_str = ["Invalid", "by Intelligence Points", "by getting the Diamond Collar",
                         "by drinking more cocktails",
                         "by spilling more cocktails", "by causing more damage", "by randomness",
                         "by being the last player ingame", "by being the only fair player"]

    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings):
        super(GameOverScreen, self).__init__(window, controller, settings)

        self.parent_view = parent
        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")
        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .45, self.settings.window_height * .75),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager
        )

        self.tb_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .05, self.settings.window_height * .05),
                                      (self.settings.window_width * .95, self.settings.window_height * .75)),
            manager=self.manager
        )

        self.__padding = self.container.rect.width / 15
        self.__buttonSize = (self.container.rect.width / 2, self.container.rect.width / 12)
        self.__labelSize = (self.container.rect.width / 3, self.container.rect.width / 15)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        logging.info("Init of GameOverScreen done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.return_button: self._return_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Could not find UI-Element in dict")

    def _return_pressed(self):
        self.controller.to_main_menu()

    def network_update(self) -> None:
        self._update_textbox()

    def _update_textbox(self) -> None:
        html_str = ""

        winner = self.controller.lib_client_handler.lib_client.getWinner()
        reason = self.controller.lib_client_handler.lib_client.getWinningReason()
        if winner.has_value() and reason.has_value():
            html_str += f"<b>{winner.value()}</b> won {self._victory_enum_str[reason]}<br><br>"

        stats = self.controller.lib_client_handler.lib_client.getStatistics()
        if stats.has_value():
            stats = stats.value()
            for stat in stats.getEntries():
                html_str += f"Metric: <b>{stat.getTitle()}</b> Description: {stat.getDescription()}" \
                            f"Player1={stat.getValuePlayerOne()} Player2={stat.getValuePlayerTwo()}<br>"

        hasReplay = self.controller.lib_client_handler.lib_client.hasReplay()
        if hasReplay.has_value():
            html_str += f"<br><br>Has replay: {hasReplay.value()}"

        self.stats_textbox.html_text = html_str
        self.stats_textbox.rebuild()

    def _init_ui_elements(self) -> None:
        self.stats_textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=self.tb_container.rect,
            manager=self.manager,
            container=self.tb_container,
            object_id="#stats_textbox"
        )

        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            text="Return to Main Menu",
            manager=self.manager,
            container=self.container,
            object_id="#return_button"
        )
