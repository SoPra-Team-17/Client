import logging
import sys
import pygame_gui.elements.ui_button
from pygame_gui.elements import UITextBox
import pygame

from view.BasicView import BasicView
from controller.ControllerView import ControllerMainMenu


class MainMenu(BasicView):
    def __init__(self, window: pygame.display, controller: ControllerMainMenu):
        super(MainMenu, self).__init__(window, controller)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), "assets/Menu/MainMenuTheme.json")
        self.manager.add_font_paths("SanistaOne", "assets/Menu/SanistaOne.ttf")

        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45, self.window_height * .45), (150, 40)),
            text="Start Game",
            manager=self.manager)
        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45, self.window_height * .5), (150, 40)),
            text="Help",
            manager=self.manager)
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45, self.window_height * .55), (150, 40)),
            text="Settings",
            manager=self.manager)
        self.end_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45, self.window_height * .6), (150, 40)),
            text="End Game",
            manager=self.manager)

        self.title_textbox = UITextBox(
            "No Time to Spy",
            pygame.Rect((self.window_width * .45, self.window_height * .25), (250, 200)),
            manager=self.manager,
        )

        logging.info("MainMenu init done")

    def draw(self):
        """
        Basic draw function for MainMenu View
        :return:    None
        """
        pygame.draw.circle(self.window, (255, 0, 0), (250, 250), 50)
        # todo delta refresh time from clock!
        self.manager.update(0.0001)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event):
        """
        Basic Interface to Controller
        Controller sends filtered events
        :param event:   filtered event from controller
        :return:    None
        """

        if (event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and
                event.ui_element == self.start_game_button):
            self.controller.start_game()

        if (event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and
                event.ui_element == self.help_button):
            pass

        if (event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and
                event.ui_element == self.settings_button):
            pass

        if (event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and
                event.ui_element == self.end_game_button):
            self.controller.exit_game()
