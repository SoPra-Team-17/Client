"""
Implements a small box displaying the current round number
"""

import pygame
import pygame_gui
import cppyy

from view.ViewSettings import ViewSettings

__author__ = "Marco Deuscher"
__date__ = "09.06.2020"


class RoundCounterBox:
    __round_counter_position = (0, 0)
    __round_counter_size = (100, 75)

    def __init__(self, parent, manager: pygame_gui.UIManager) -> None:
        self.parent_screen = parent
        self.manager = manager

        self.textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(self.__round_counter_position, self.__round_counter_size),
            manager=self.manager,
            object_id="#round_counter_tb"
        )

    def update_textbox(self) -> None:
        """
        Implements interface to parent screen to update displayed round number
        :return:    None
        """
        self._update_textbox()

    def _update_textbox(self) -> None:
        current_round = self.parent_screen.controller.lib_client_handler.lib_client.getState().getCurrentRound()
        max_round = self.parent_screen.controller.lib_client_handler.lib_client.getSettings().getRoundLimit()

        html_str = f"<b>Round</b><br>{current_round}/{max_round}"
        self.textbox.html_text = html_str
        self.textbox.rebuild()
