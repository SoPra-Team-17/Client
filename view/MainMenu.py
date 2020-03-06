import logging
import pygame_gui.elements.ui_button
from pygame_gui.elements import UITextBox
import pygame

import view.ViewConstants as props
from view.BasicView import BasicView
from controller.ControllerView import ControllerMainMenu


# todo positionen sind noch hardcoded --> relatives layout oder verwenden von layout manager
# todo Skalierung der Größe der Buttons muss mit der Auflösung gehen, da muss mal bisschen Mathematik betrieben werden
class MainMenu(BasicView):
    def __init__(self, window: pygame.display, controller: ControllerMainMenu):
        super(MainMenu, self).__init__(window, controller)

        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height),
                                            "assets/Menu/MainMenuTheme.json")
        self.manager.add_font_paths("SanistaOne", "assets/Menu/SanistaOne.ttf")

        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))
        # layout manger verwenden bspw. grid layout
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45,
                                       self.window_height * .45), (150, 40)),
            text="Start Game",
            manager=self.manager)
        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45,
                                       self.window_height * .5), (150, 40)),
            text="Help",
            manager=self.manager)
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45,
                                       self.window_height * .55), (150, 40)),
            text="Settings",
            manager=self.manager)
        self.end_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width * .45,
                                       self.window_height * .6), (150, 40)),
            text="End Game",
            manager=self.manager)

        self.title_textbox = UITextBox(
            "No Time to Spy",
            pygame.Rect((self.window_width * .45,
                         self.window_height * .25), (250, 200)),
            manager=self.manager,
        )

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
        self.manager.draw_ui(self.window)

        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event):
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed':
            switcher = {
                self.start_game_button: self.controller.start_game,
                self.end_game_button: self.controller.exit_game
            }
            switcher.get(event.ui_element)()
