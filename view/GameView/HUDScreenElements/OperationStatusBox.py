"""
Implements infobox which displays the result of the last operation
"""

import logging
import pygame
import pygame_gui
import cppyy

from cppyy import addressof, bind_object

from view.ViewSettings import ViewSettings

__author__ = "Marco Deuscher"
__date__ = "07.06.2020 (creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/Point.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")
cppyy.include("util/GameLogicUtils.hpp")
cppyy.include("datatypes/gameplay/OperationEnum.hpp")
cppyy.include("datatypes/gameplay/Movement.hpp")


class OperationStatusBox:
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    __button_size = (150, 35)

    def __init__(self, parent, container: pygame_gui.core.UIContainer, manager: pygame_gui.UIManager,
                 settings: ViewSettings) -> None:
        self.parent_screen = parent
        self.container = container
        self.manager = manager
        self.settings = settings

        self.textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__distance - self.__button_size[0] - self.__info_textbox_width -
                 3 * self.__button_size[0], 0),
                (self.__info_textbox_width, self.container.rect.height)),
            manager=self.manager,
            container=self.container,
            object_id="#operation_status_textbox"
        )

        self.__prev_valid = False
        self.__prev_successfull = False
        self.__keys = 0

        self.__box_str = ""

    def update_valid_op(self, was_valid: bool) -> None:
        self.__prev_valid = was_valid

        self._update_textbox()

    def update_successfull_op(self) -> None:
        op_vec = self.parent_screen.controller.lib_client_handler.lib_client.getOperations()

        if op_vec.empty():
            return

        # todo when libclient pr is done, get isenemy pair and lastOpSuccessfull and display!

    def update_textbox(self) -> None:
        """
        Interface to screen to udpate textbox
        :return:    None
        """
        self.update_textbox()

    def _update_textbox(self) -> None:
        self.__box_str = ""

        if self.__prev_valid:
            self.__box_str += "Operation was <b>valid</b><br><br>"
        else:
            self.__box_str += "Operation was <b>not valid</b><br><br>"

        safe_combs = self.parent_screen.controller.lib_client_handler.lib_client.getState().getMySafeCombinations()
        self.__box_str += f"Team has <b>{safe_combs.size()}</b> safe combinations<br>"

        self.textbox.html_text = self.__box_str
        self.textbox.rebuild()
