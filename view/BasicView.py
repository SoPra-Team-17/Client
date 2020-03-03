from abc import ABC, abstractmethod
import pygame



class BasicView(ABC):
    def __init__(self, window: pygame.display, controller):
        self.window = window
        self.controller = controller

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def receive_event(self, event: pygame.event.Event):
        pass

