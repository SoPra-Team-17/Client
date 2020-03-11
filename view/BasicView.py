from abc import ABC, abstractmethod
import pygame


class BasicView(ABC):
    """
    Defines abstract interface for any view
    """

    def __init__(self, window: pygame.display, controller):
        self.window = window
        self.controller = controller


    @abstractmethod
    def draw(self):
        """
        Basic draw function for MainMenu View
        :return:    None
        """

    @abstractmethod
    def receive_event(self, event: pygame.event.Event):
        """
        Basic Interface to Controller
        Controller sends filtered events
        :param event:   filtered event from controller
        :return:    None
        """
