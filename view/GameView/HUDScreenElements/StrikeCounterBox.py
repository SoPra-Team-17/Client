"""
Implements textbox displaying number of received strike and max. number of strikes
"""
import pygame
import pygame_gui

__author__ = "Marco Deuscher"
__date__ = "09.06.2020"


class StrikeCounterBox:
    __strike_box_position = (300, 0)
    __strike_box_size = (100, 75)

    def __init__(self, parent, manager: pygame_gui.UIManager) -> None:
        self.parent_screen = parent
        self.manager = manager

        self.textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(self.__strike_box_position, self.__strike_box_size),
            manager=self.manager,
            object_id="#strike_display_textbox"
        )

    def update_textbox(self) -> None:
        strike_nr = self.parent_screen.controller.lib_client_handler.lib_client.getStrikeNr()
        strike_max = self.parent_screen.controller.lib_client_handler.lib_client.getStrikeMax()

        html_str = f"<b>Strike</b><br>{strike_nr}/{strike_max}"
        self.textbox.html_text = html_str
        self.textbox.rebuild()
