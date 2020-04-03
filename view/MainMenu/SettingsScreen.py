import logging
import pygame_gui.elements.ui_button
import pygame

import view.ViewConstants as props
from view.BasicView import BasicView
from controller.ControllerView import ControllerMainMenu


class SettingsScreen(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, parentView):
        super(SettingsScreen, self).__init__(window, controller)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height),
                                            "assets/Menu/MainMenuTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.window_width * .17, self.window_height * .1),
                                      (self.window_width / 4, self.window_height / 2)),
            manager=self.manager)

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self.button01 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Button01",
            manager=self.manager,
            container=self.container
        )
        self.button02 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Button02",
            manager=self.manager,
            container=self.container
        )
        self.button03 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Button03",
            manager=self.manager,
            container=self.container
        )
        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Return",
            manager=self.manager,
            container=self.container
        )

        logging.info("Settings Screen init done")

    def draw(self) -> None:
        self.manager.update(1 / props.FRAME_RATE)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == "ui_button_pressed":
            switcher = {
                self.button01: self.default_callback,
                self.button02: self.default_callback,
                self.button03: self.default_callback,
                self.return_button:  self.return_button_pressed
            }
            switcher.get(event.ui_element)()

    def default_callback(self) -> None:
        logging.info("Button pressed")

    def return_button_pressed(self) -> None:
        self.parent_view.to_main_menu()
