import logging
import pygame

from view.BasicView import BasicView
from view.Lobby.LobbyScreen import LobbyScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerLobby


class LobbyView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerLobby, settings: ViewSettings) -> None:
        super(LobbyView, self).__init__(window, controller, settings)

        self.active_screens = []

        self.lobby_screen = LobbyScreen(window, controller, self, settings)

        self.active_screens.append(self.lobby_screen)

        logging.info("Lobby init done")

    def draw(self) -> None:
        for screen in self.active_screens:
            screen.draw()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        for screen in self.active_screens:
            screen.receive_event(event)
