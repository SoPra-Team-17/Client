"""
Implements infobox which displays past operations
"""
import logging
import pygame
import pygame_gui
import cppyy

from view.ViewSettings import ViewSettings

__author__ = "Marco Deuscher"
__date__ = "08.06.2020 (creation)"


class OperationLogBox:
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    __button_size = (150, 35)

    def __init__(self, parent, container: pygame_gui.core.UIContainer, manager: pygame_gui.UIManager,
                 setttings: ViewSettings) -> None:
        self.parent_screen = parent
        self.container = container
        self.manager = manager
        self.settings = setttings

        self.textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__distance - self.__button_size[
                    0] * .75 - 2 * self.__info_textbox_width -
                 3 * self.__button_size[0], 0),
                (self.__info_textbox_width, self.container.rect.height)),
            manager=self.manager,
            container=self.container,
            object_id="#operation_log_box"
        )

        self.__info_str = ""

    def update_textbox(self) -> None:
        """
        Interface to screen to update textbox
        :return:
        """
        self._update_textbox()

    def _update_textbox(self) -> None:
        info_str = ""
        operation_vec = self.parent_screen.controller.lib_client_handler.lib_client.getOperations()
        if operation_vec.empty():
            return

        for operation in operation_vec:
            info_str += f"<b>Operation:</b>{self.parent_screen.controller.lib_client_handler.lib_client.operationToString(operation)}<br><br>"

        self.__info_str = info_str + self.__info_str

        self.textbox.html_text = self.__info_str
        self.textbox.rebuild()
