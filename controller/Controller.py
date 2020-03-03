"""
@brief  some module String
"""
import sys
import logging
import pygame
import view.ViewConstants as props
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
        self.screen = pygame.display.set_mode((props.WINDOW_WIDTH, props.WINDOW_HEIGHT))
        pygame.display.set_caption(props.WINDOW_NAME)
        self.clock = pygame.time.Clock()
        self.mainMenu = MainMenu(self.screen, self)

    def init_components(self):
        """
        @brief  initializes all other components
        """
        # initialize components (model,view,self)
        logging.info("Controller init done")

    def loop(self):
        """
        :brief: basic main loop
        :return:
        """
        # main game loop is started from here
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                # todo sinnvolles filtern der events
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.USEREVENT:
                    self.mainMenu.receive_event(event)
                #todo muss irgendwo anders hin
                self.mainMenu.manager.process_events(event)
            # todo sollte in view
            self.mainMenu.draw()

            self.clock.tick(props.FRAME_RATE)

    def start_game(self):
        logging.info("StartGame in MainMenu View pressed")
    def exit_game(self):
        pass
    def send_action(self):
        pass
