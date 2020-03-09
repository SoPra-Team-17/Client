import sys
import logging
import pygame
import view.ViewConstants as props
from view.MainMenu import MainMenu
from controller.ControllerView import ControllerGameView, ControllerMainMenu


class Controller(ControllerGameView, ControllerMainMenu):
    """
    class implementing a basic controller
    """

    def __init__(self):
        # call init of ControllerGameView
        super(Controller, self).__init__()
        # call init of ControllerMainMenu
        super(ControllerGameView, self).__init__()

        pygame.init()
        # erstelle screen
        self.screen = pygame.display.set_mode((props.WINDOW_WIDTH, props.WINDOW_HEIGHT))
        pygame.display.set_caption(props.WINDOW_NAME)
        self.clock = pygame.time.Clock()
        self.mainMenu = MainMenu(self.screen, self)
        self.activeViews = []

        # at the beginning main menu is the active view
        self.activeViews.append(self.mainMenu)

    def init_components(self):
        """
        initializes all other components
        Calls init of view
        """
        # initialize components (model,view,self)
        logging.info("Controller init done")

    def loop(self):
        """
        basic main loop
        :return:    None
        """
        # main game loop is started from here
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                # distribute events to all active views
                for view in self.activeViews:
                    view.receive_event(event)
            # drawing order to all active views
            for view in self.activeViews:
                view.draw()

            self.clock.tick(props.FRAME_RATE)

    def start_game(self):
        logging.info("Start game detected")

    def exit_game(self):
        logging.info("Exit from MainMenu")
        pygame.quit()
        sys.exit(0)

    def send_action(self):
        pass
