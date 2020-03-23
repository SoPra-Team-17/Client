from abc import ABC, abstractmethod
import pygame


class BasicView(ABC):
    """
    Defines abstract interface for any view
    """

    def __init__(self, window: pygame.display, controller) -> None:
        self.window = window
        self.controller = controller


    @abstractmethod
    def draw(self) -> None:
        """
        Basic draw function for MainMenu View
        :return:    None
        """

    @abstractmethod
    def receive_event(self, event: pygame.event.Event) -> None:
        """
        Basic Interface to Controller
        Controller sends filtered events
        :param event:   filtered event from controller
        :return:    None
        """
