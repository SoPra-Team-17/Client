"""
@brief  some module String
"""
import sys
import logging
import pygame
from view.MainMenu import MainMenu
from controller.ControllerView import ControllerGameView, ControllerMainMenu


class Controller(ControllerGameView, ControllerMainMenu):
    """
    @brief  class implementing a basic controller
    """

    def __init__(self):
        super().__init__()
        pygame.init()
        # erstelle screen
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("No Time to Spy")
        self.clock = pygame.time.Clock()
        self.mainMenu = MainMenu(self.screen, self)

    def init_components(self):
        """
        initializes all other components
        """
        # initialize components (model,view,self)
        logging.info("Controller init done")

    def loop(self):
        """
        basic main loop
        :return:
        """
        # main game loop is started from here
        while True:
            # events should be filtered
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mainMenu.receive_event(event)

            # todo extension for other views!
            self.mainMenu.draw()

            self.clock.tick(60)

    def start_game(self):
        """
        Interface to MainMenu View
        :return:    None
        """
        print("Press detected")

    def exit_game(self):
        """
        Interface to MainMenu View
        :return:    None
        """
        pass

    def send_action(self):
        """
        Interface to GameView
        :return:    None
        """
        pass
