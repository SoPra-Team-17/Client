"""
Defines the basic interface of a view
"""
from abc import ABC, abstractmethod
import pygame
from view.ViewSettings import ViewSettings

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class BasicView(ABC):
    """
    Defines abstract interface for any view
    """

    def __init__(self, window: pygame.display, controller, settings: ViewSettings) -> None:
        self.window = window
        self.controller = controller
        self.settings = settings

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
