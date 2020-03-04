from abc import ABC, abstractmethod
import pygame


class BasicView(ABC):
    """
    Defines abstract interface for any view
    """
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def receive_event(self, event: pygame.event.Event):
        pass
