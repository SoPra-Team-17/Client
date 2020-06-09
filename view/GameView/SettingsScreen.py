"""
Implements the gameview settings screen
"""
import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView

__author__ = "Marco Deuscher"
__date__ = "02.06.2020 (creation)"


class SettingsScreen(BasicView):
    _text_buttons = {
        "pause_game": "Pause Game",
        "leave_game": "Leave Game",
        "return": "Return to Game"
    }

    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings) -> None:
        super(SettingsScreen, self).__init__(window, controller, settings)
        self.parent_view = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .45, self.settings.window_height * .4),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager
        )

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 2, self.container.rect.width / 12)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        logging.info("Game view Settings Screen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)
        self._update_label()

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.pause_game_button: self._pause_pressed,
                self.leave_game_button: self._leave_pressed,
                self.return_to_game_button: self._return_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Did not find UI-Element in dict")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._return_pressed()

    def _pause_pressed(self):
        # toggle game paused
        paused = self.controller.lib_client_handler.lib_client.isGamePaused()
        ret = self.controller.send_request_game_pause(not paused)
        logging.info(f"Successfully sent pause_message: {ret}")

    def _leave_pressed(self):
        ret = self.controller.send_game_leave()
        logging.info(f"Successfully sent game leave message: {ret}")
        if ret:
            self.controller.to_main_menu()

    def _return_pressed(self):
        self.parent_view.parent.to_playing_field()

    def _update_label(self) -> None:
        paused = self.controller.lib_client_handler.lib_client.isGamePaused()
        label_str = "Game is paused" if paused else "Game is not paused"
        self.pause_state_label.set_text(label_str)

    def _init_ui_elements(self):
        self.pause_state_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            text="",
            manager=self.manager,
            container=self.container,
            object_id="#pause_state_label"
        )

        self.pause_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            text=self._text_buttons["pause_game"],
            manager=self.manager,
            container=self.container,
            object_id="#pause_button"
        )

        self.leave_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            text=self._text_buttons["leave_game"],
            manager=self.manager,
            container=self.container,
            object_id="#leave_button"
        )

        self.return_to_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            text=self._text_buttons["return"],
            manager=self.manager,
            container=self.container,
            object_id="#return_button"
        )
