"""
Implements the gameview settings screen
"""
import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "02.06.2020 (creation)"


class SettingsScreen(BasicView):
    _text_buttons = {
        "pause_game": "Pause Game",
        "unpause_game": "Unpause Game",
        "leave_game": "Leave Game",
        "return": "Return to Game",
        "shortcuts": "Shortcuts"
    }

    _shortcuts_help_str = "<b>Shortcuts</b><br><br>" \
                          "<b>Actions</b><br>" \
                          "m: Movement<br>g: Gadget<br>b: Gamble<br>e: Spy<br>p: Property<br>r: Retire<br>" \
                          "<br><b>Execution</b><br>" \
                          "enter: send action<br>"

    __shortcuts_position = (200, 200)
    __shortcuts_size = (250, 280)

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
                self.return_to_game_button: self._return_pressed,
                self.shortcuts_help_button: self._update_shortcuts_textbox
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Did not find UI-Element in dict")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._return_pressed()

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GamePause":
                self._update_label()

    def _pause_pressed(self) -> None:
        """
        Function called when pause/unpause button is pressed
        :return:    None
        """
        # toggle game paused
        paused = self.controller.lib_client_handler.lib_client.isGamePaused()
        ret = self.controller.send_request_game_pause(not paused)
        logging.info(f"Successfully sent pause_message: {ret}")

    def _leave_pressed(self) -> None:
        """
        Function called when leave game button is pressed
        :return:    None
        """
        ret = self.controller.send_game_leave()
        logging.info(f"Successfully sent game leave message: {ret}")
        if ret:
            self.controller.to_main_menu()

    def _return_pressed(self) -> None:
        """
        Function called when return to playing field button is pressed
        :return:    None
        """
        self.parent_view.parent.to_playing_field()

    def _update_label(self) -> None:
        """
        Function updating label of UILabel and UIButton
        Displays pause/unpause based on current state
        :return:    None
        """
        paused = self.controller.lib_client_handler.lib_client.isGamePaused()
        label_str = "Game is paused" if paused else "Game is not paused"
        self.pause_state_label.set_text(label_str)
        key = "unpause_game" if paused else "pause_game"
        self.pause_game_button.set_text(self._text_buttons.get(key))

    def _update_shortcuts_textbox(self) -> None:
        """
        Updates shortcuts textbox, when shortcut button is pressed
        :return:    None
        """
        if self.shortcuts_help_textbox is not None:
            self.shortcuts_help_textbox.kill()
            self.shortcuts_help_textbox = None
            return

        self.shortcuts_help_textbox = pygame_gui.elements.UITextBox(
            html_text=self._shortcuts_help_str,
            relative_rect=pygame.Rect(self.__shortcuts_position, self.__shortcuts_size),
            manager=self.manager,
            object_id="#shortcut_textbox"
        )

    def _init_ui_elements(self):
        self.shortcuts_help_textbox = None

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

        self.shortcuts_help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            text=self._text_buttons["shortcuts"],
            manager=self.manager,
            container=self.container,
            object_id="#shortcuts_button"
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
