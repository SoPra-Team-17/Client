"""
Implements infobox which displays the result of the last operation
"""

import pygame
import pygame_gui
import cppyy

from cppyy.gbl.std import vector

from view.ViewSettings import ViewSettings

__author__ = "Marco Deuscher"
__date__ = "07.06.2020 (creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")


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
                (self.container.rect.width - self.__distance - self.__button_size[0] * .75 - self.__info_textbox_width -
                 3 * self.__button_size[0], 0),
                (self.__info_textbox_width, self.container.rect.height)),
            manager=self.manager,
            container=self.container,
            object_id="#operation_status_textbox"
        )

        self.__prev_valid = False
        self.__prev_successfull = False
        self.__is_enemy = None
        self.__keys = 0

        self.__box_str = ""

    def update_valid_op(self, was_valid: bool) -> None:
        self.__prev_valid = was_valid

        self._update_textbox()

    def update_successfull_op(self) -> None:
        op_vec = self.parent_screen.controller.lib_client_handler.lib_client.getOperations()

        if op_vec.empty():
            return

        self.__prev_successfull = self.parent_screen.controller.lib_client_handler.lib_client.lastOpSuccessful()
        self.__is_enemy = self.parent_screen.controller.lib_client_handler.lib_client.isEnemy()
        self._update_textbox()

    def update_textbox(self) -> None:
        """
        Interface to screen to update textbox
        :return:    None
        """
        self._update_textbox()

    def _update_textbox(self) -> None:
        self.__box_str = ""

        if self.__prev_valid:
            self.__box_str += "Operation was <b>valid</b><br><br>"
        else:
            self.__box_str += "Operation was <b>not valid</b><br><br>"

        if self.__prev_successfull:
            self.__box_str += "Last valid operation was <b>successful</b><br><br>"
        else:
            self.__box_str += "Last valid operation was <b>not successful</b><br><br>"

        safe_combs = self.parent_screen.controller.lib_client_handler.lib_client.getState().getMySafeCombinations()
        self.__box_str += f"Team has <b>{safe_combs.size()}</b> safe combinations<br>"

        if self.__is_enemy is not None and self.__is_enemy.has_value():
            is_enemy = self.__is_enemy.value()
            # character id (second) and isEnemy (first)
            char_id = is_enemy.second
            enemy = is_enemy.first

            # get name of character
            info = self.parent_screen.controller.lib_client_handler.lib_client.getInformation()
            variant = info[
                cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
            char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)
            name = ""
            for char_info in char_info_vector:
                if char_id == char_info.getCharacterId():
                    name = char_info.getName()
                    break

            self.__box_str += f"{name} is enemy: <b>{enemy}</b>"

        self.textbox.html_text = self.__box_str
        self.textbox.rebuild()
