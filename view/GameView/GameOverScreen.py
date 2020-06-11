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
        self.tb_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .1, self.settings.window_height * .05),
                                      (self.settings.window_width * .75, self.settings.window_height * .85)),
            manager=self.manager
        )

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

        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self._return_pressed()

    def _return_pressed(self):
        ret = self.controller.send_game_leave()
        logging.info(f"Successfully send game leave: {ret}")
        self.controller.to_main_menu()

    def network_update(self) -> None:
        self._update_textbox()

    def _update_textbox(self) -> None:
        html_str = ""

        winner = self.controller.lib_client_handler.lib_client.getWinner()
        reason = self.controller.lib_client_handler.lib_client.getWinningReason()
        if winner.has_value() and reason.has_value():
            winner_name = ""
            if winner.value == self.controller.lib_client_handler.lib_client.getPlayerOneId():
                winner_name = self.controller.lib_client_handler.lib_client.getPlayerOneName()
            else:
                winner_name = self.controller.lib_client_handler.lib_client.getPlayerTwoName()

            html_str += f"<b>{winner_name} won {self._victory_enum_str[reason.value()]}</b><br><br><br>"

        stats = self.controller.lib_client_handler.lib_client.getStatistics()
        if stats.has_value():
            p1_name = self.controller.lib_client_handler.lib_client.getPlayerOneName()
            p2_name = self.controller.lib_client_handler.lib_client.getPlayerTwoName()
            stats = stats.value()
            for stat in stats.getEntries():
                html_str += f"Metric: <b>{stat.getTitle()}</b><br>Description: {stat.getDescription()}<br>" \
                            f"{p1_name}={stat.getValuePlayerOne()}<br>{p2_name}={stat.getValuePlayerTwo()}<br><br>"

        hasReplay = self.controller.lib_client_handler.lib_client.hasReplay()
        html_str += f"<br><br>Has replay: {hasReplay}<br><br>"
        html_str += f"Return to Main Menu by pressing <b>Escape</b><br>"

        self.stats_textbox.html_text = html_str
        self.stats_textbox.rebuild()

    def _init_ui_elements(self) -> None:
        self.stats_textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect((0, 0), (self.tb_container.rect.width, self.tb_container.rect.height)),
            manager=self.manager,
            container=self.tb_container,
            object_id="#stats_textbox"
        )
