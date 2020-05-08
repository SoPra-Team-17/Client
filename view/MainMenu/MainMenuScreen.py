"""
Implements the actual MainMenu screen
"""
import logging
import pygame_gui.elements.ui_button
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class MainMenuScreen(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, parentView,
                 settings: ViewSettings) -> None:
        super(MainMenuScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/Menu/MainMenuTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .375, self.settings.window_height * .4),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager)

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        # load title image
        self.titleImage = pygame.image.load("assets/Menu/TitleImage.png")
        logging.info("MainMenuScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.titleImage,
                         (self.settings.window_width / 2 - self.titleImage.get_rect().width / 2,
                          self.settings.window_height * .25))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.start_game_button: self.start_game_pressed,
                self.help_button: self.help_button_pressed,
                self.settings_button: self.settings_button_pressed,
                self.end_game_button: self.controller.exit_game
            }
            switcher.get(event.ui_element)()

    def start_game_pressed(self) -> None:
        # todo uncomment to have network connection
        # self.controller.connect_to_server(self.settings.address, self.settings.port)
        self.controller.start_game()

    def help_button_pressed(self) -> None:
        self.parent_view.help_button_pressed()

    def settings_button_pressed(self) -> None:
        self.parent_view.to_settings()

    def _init_ui_elements(self) -> None:
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.container.get_size()[0] / 2.75, self.__padding * len(self.container.elements)),
                self.__buttonSize),
            text="Start Game",
            manager=self.manager,
            container=self.container
        )

        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.get_size()[0] / 2.75,
                                       self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Help",
            manager=self.manager,
            container=self.container
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.get_size()[0] / 2.75,
                                       self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Settings",
            manager=self.manager,
            container=self.container
        )
        self.end_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.get_size()[0] / 2.75,
                                       self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="End Game",
            manager=self.manager,
            container=self.container
        )
