import logging
import pygame_gui.elements.ui_button
from pygame_gui.elements import UITextBox
import pygame

import view.ViewConstants as props
from view.BasicView import BasicView
from controller.ControllerView import ControllerMainMenu


class MainMenu(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerMainMenu):
        super(MainMenu, self).__init__(window, controller)

        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height),
                                            "assets/Menu/MainMenuTheme.json")
        self.manager.add_font_paths("SanistaOne", "assets/Menu/SanistaOne.ttf")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.window_width * .15, self.window_height * .1),
                                      (self.window_width / 4, self.window_height / 2)),
            manager=self.manager)

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Start Game",
            manager=self.manager,
            container=self.container
        )
        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Help",
            manager=self.manager,
            container=self.container
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Settings",
            manager=self.manager,
            container=self.container
        )
        self.end_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="End Game",
            manager=self.manager,
            container=self.container
        )

        # load title image
        self.titleImage = pygame.image.load("assets/Menu/TitleImage.png")

        logging.info("MainMenu init done")

    def init(self):
        """
        Not yet implemented
        :return:    None
        """

    def draw(self):
        pygame.draw.circle(self.window, (255, 0, 0), (250, 250), 50)
        self.manager.update(1 / props.FRAME_RATE)

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.titleImage,
                         (self.window_width / 2 - self.container.rect.width / 2, self.window_height * .25))
        self.manager.draw_ui(self.window)

        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event):
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed':
            switcher = {
                self.start_game_button: self.controller.start_game,
                self.help_button: self.help_button_pressed,
                self.settings_button: self.settings_button_pressed,
                self.end_game_button: self.controller.exit_game
            }
            switcher.get(event.ui_element)()

    def help_button_pressed(self):
        pass

    def settings_button_pressed(self):
        pass
