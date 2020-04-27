import sys
import logging
import pygame
from view.ViewSettings import ViewSettings
from view.MainMenu.MainMenu import MainMenu
from view.GameView.GameView import GameView
from view.Lobby.LobbyView import LobbyView
from controller.ControllerView import ControllerGameView, ControllerMainMenu, ControllerLobby
from controller.ControllerNetworkInterface import ControllerNetworkInterface
from network.LibClientHandler import LibClientHandler



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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VIEW SWITCHES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SEND NETWORK MESSAGE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # LobbyView Messages
    def connect_to_server(self, servername: str, port: int) -> bool:
        return self.lib_client_handler.connect(servername, port)

    def send_reconnect(self) -> bool:
        return self.lib_client_handler.sendReconnect()

    def send_hello(self, name, role) -> bool:
        return self.lib_client_handler.sendHello(name, role)

    # GameView Messages
    def sendItemChoice(self, choice) -> bool:
        return self.lib_client_handler.sendItemChoice(choice)

    def sendEquipmentChoice(self, equipMap) -> bool:
        return self.lib_client_handler.sendEquipmentChoice(equipMap)

    def sendGameOperation(self, operation) -> bool:
        return self.lib_client_handler.sendGameOperation(operation)

    def sendGameLeave(self) -> bool:
        return self.lib_client_handler.sendGameLeave()

    def sendRequestGamePause(self, gamePause: bool) -> bool:
        return self.lib_client_handler.sendRequestGamePause(gamePause)

    def sendRequestMetaInformation(self, keys) -> bool:
        return self.lib_client_handler.sendRequestMetaInformation(keys)

    def sendRequestReplay(self) -> bool:
        return self.lib_client_handler.sendRequestReplay()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NETWORK MESSAGE CALLBACK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onHelloReply(self) -> None:
        logging.info("Received hello reply message")

    def onGameStarted(self) -> None:
        logging.info("Received game started message")

    def onRequestChoice(self) -> None:
        logging.info("Recieved request choice message")

    def onRequestEquipmentChoice(self) -> None:
        logging.info("Received request eq. choice message")

    def onGameStatus(self) -> None:
        logging.info("Received game status message")

    def onRequestGameOperation(self) -> None:
        logging.info("Received request game operation message")

    def onStatistics(self) -> None:
        logging.info("Received statistics message")

    def onGameLeft(self) -> None:
        logging.info("Recieved game left message")

    def onGamePause(self) -> None:
        logging.info("Received game pause message")

    def onMetaInformation(self) -> None:
        logging.info("Received meta information message")

    def onStrike(self) -> None:
        logging.info("Received strike message")

    def onErrorMessage(self) -> None:
        logging.info("Received error message")

    def onReplay(self) -> None:
        logging.info("Received replay message")
