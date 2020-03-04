import pygame
from view.BasicView import BasicView
from controller.ControllerView import ControllerMainMenu


class MainMenu(BasicView):
    def __init__(self, window, controller: ControllerMainMenu):
        super(MainMenu, self).__init__(window, controller)

    def draw(self):
        """
        Basic draw function for MainMenu View
        :return:    None
        """
        pygame.draw.circle(self.window, (255, 0, 0), (250, 250), 50)
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event):
        """
        Basic Interface to Controller
        Controller sends filtered events
        :param event:   filtered event from controller
        :return:    None
        """
        print(pygame.mouse.get_pos())
        pos = pygame.mouse.get_pos()
        if pos[0] > 200 and pos[1] > 200:
            self.controller.start_game()
