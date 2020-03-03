from view.BasicView import BasicView
from controller.ControllerView import ControllerMainMenu
import pygame_gui.elements.ui_button
import pygame
import logging
import sys


class MainMenu(BasicView):
    def __init__(self, window, controller: ControllerMainMenu):
        super(MainMenu, self).__init__(window, controller)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), "assets/Menu/MainMenuTheme.json")

        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self.start_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 280), (150, 40)),
                                                    text="Start Game",
                                                    manager=self.manager)
        self.end_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 380), (150, 40)),
                                                              text="End Game",
                                                              manager=self.manager)

        logging.info("MainMenu init done")


    def draw(self):
        pygame.draw.circle(self.window, (255, 0, 0), (250, 250), 50)
        #todo delta refresh time from clock!
        self.manager.update(0.0001)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

        pygame.display.update()
        pygame.display.flip()


    def receive_event(self, event: pygame.event.Event):
        print(pygame.mouse.get_pos())
        pos = pygame.mouse.get_pos()
        print(event.type)

        if (event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and
                event.ui_element == self.start_game_button):
            print('Hello World!')
        if (event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and
                event.ui_element == self.end_game_button):
            pygame.quit()
            sys.exit(0)


