import pygame
import pygame_gui

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class HUDView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings) -> None:
        super(HUDView, self).__init__(window, controller, settings)



    def draw(self) -> None:
        pass

    def receive_event(self, event: pygame.event.Event) -> None:
        pass
