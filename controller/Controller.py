import sys
import logging
import pygame
from view.ViewSettings import ViewSettings
from view.MainMenu.MainMenu import MainMenu
from view.GameView.GameView import GameView
from view.Lobby.LobbyView import LobbyView
from controller.ControllerView import ControllerGameView, ControllerMainMenu, ControllerLobby
from network.LibClientHandler import LibClientHandler
from controller.ControllerNetworkInterface import ControllerNetworkInterface


class Controller(ControllerGameView, ControllerMainMenu, ControllerLobby, ControllerNetworkInterface):
    """
    class implementing a basic controller
    """

    def __init__(self) -> None:
        # call init of ControllerGameView
        super(Controller, self).__init__()
        # call init of ControllerMainMenu
        super(ControllerGameView, self).__init__()
        super(ControllerNetworkInterface, self).__init__()


        self.lib_client_handler = LibClientHandler(self)

        self.view_settings = ViewSettings()

        pygame.init()
        # erstelle screen
        self.screen = pygame.display.set_mode((self.view_settings.window_width, self.view_settings.window_height),
                                              pygame.RESIZABLE)
        pygame.display.set_caption(self.view_settings.window_name)
        self.clock = pygame.time.Clock()
        self.mainMenu = MainMenu(self.screen, self, self.view_settings)
        self.gameView = GameView(self.screen, self, self.view_settings)
        self.lobbyView = LobbyView(self.screen, self, self.view_settings)

        self.activeViews = []

        # at the beginning main menu is the active view
        self.activeViews.append(self.mainMenu)

    def init_components(self) -> None:
        """
        initializes all other components
        Calls init of view
        """
        # initialize components (model,view,self)
        logging.info("Controller init done")

    def loop(self) -> None:
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

            self.clock.tick(self.view_settings.frame_rate)

    def start_game(self) -> None:
        logging.info("Start game detected")
        self.activeViews = [self.lobbyView]

    def to_game_view(self) -> None:
        self.activeViews = [self.gameView]

    def exit_game(self) -> None:
        logging.info("Exit from MainMenu")
        pygame.quit()
        sys.exit(0)

    def to_main_menu(self) -> None:
        self.activeViews = [self.mainMenu]

    def send_action(self) -> None:
        pass

    def send_reconnect(self) -> None:
        pass

    def send_hello(self) -> None:
        pass

    def onHelloReply(self):
        pass

    def onGameStarted(self):
        pass

    def onRequestChoice(self):
        pass

    def onRequestEquipmentChoice(self):
        pass

    def onGameStatus(self):
        pass

    def onRequestGameOperation(self):
        pass

    def onStatistics(self):
        pass

    def onGameLeft(self):
        pass

    def onGamePause(self):
        pass

    def onMetaInformation(self):
        pass

    def onStrike(self):
        pass

    def onErrorMessage(self):
        pass

    def onReplay(self):
        pass
