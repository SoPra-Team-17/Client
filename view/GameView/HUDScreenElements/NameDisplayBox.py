"""
Implements a textbox displaying the names of player 1 and 2
"""
import pygame
import pygame_gui

__author__ = "Marco Deuscher"
__date__ = "09.06.2020"


class NameDisplayBox:
    __name_box_position = (100, 0)
    __name_box_size = (200, 75)

    def __init__(self, parent_screen, manager: pygame_gui.UIManager) -> None:
        self.parent_screen = parent_screen
        self.manager = manager

        self.textbox = None

    def init_textbox(self) -> None:
        p1_name = self.parent_screen.controller.lib_client_handler.lib_client.getPlayerOneName()
        p2_name = self.parent_screen.controller.lib_client_handler.lib_client.getPlayerTwoName()
        html_str = f"<b>{p1_name[:15]}</b> (P1)<br><b>{p2_name[:15]}</b> (P2)"

        self.textbox = pygame_gui.elements.UITextBox(
            html_text=html_str,
            relative_rect=pygame.Rect(self.__name_box_position, self.__name_box_size),
            manager=self.manager,
            object_id="#name_display_box"
        )
