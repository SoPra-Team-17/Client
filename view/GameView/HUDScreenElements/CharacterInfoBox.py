"""
Implements character info box which displays information about the character (e.g. name, chips, ip, etc.)
"""
import pygame_gui
import pygame
import cppyy

from cppyy.gbl.std import map, pair, set, vector

__author__ = "Marco Deuscher"
__date__ = "02.06.20 (creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/Point.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")


class CharacterInfoBox:
    __distance = 10
    # size of gadget and property icons
    __icon_size = 32

    def __init__(self, parent, container: pygame_gui.core.UIContainer, manager: pygame_gui.UIManager) -> None:
        self.parent_screen = parent
        self.container = container
        self.manager = manager
        self.private_textbox = None

        self.__padding = (self.container.rect.width / 2 - 5 * self.__distance) / 7

    def update_textbox(self, idx) -> None:
        """
        Interface to parent screen
        :param idx:     index of hovered character
        :return:        None
        """
        self._init_private_textbox(idx)

    def reset(self) -> None:
        """
        Interface to parent screen
        Box has to be redrawn each time
        :return:    None
        """
        if self.private_textbox is not None:
            self.private_textbox.kill()
            self.private_textbox = None

    def _init_private_textbox(self, idx) -> None:
        """
        Creates a new textbox, which displays relevant information. Is placed above the hovered character image
        todo properly format textboxes
        :param idx:     Idx of hovered character in UI-List
        :return:        None
        """
        char_id = self.parent_screen.controller.lib_client_handler.lib_client.getChosenCharacters()[idx]
        char = self.parent_screen.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            char_id)

        hp = char.getHealthPoints()
        chips = char.getChips()
        ip = char.getIntelligencePoints()
        info = self.parent_screen.controller.lib_client_handler.lib_client.getInformation()
        variant = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)

        chosen_char_id = self.parent_screen.controller.lib_client_handler.lib_client.getChosenCharacters()[idx]
        name = ""
        for char_info in char_info_vector:
            if chosen_char_id == char_info.getCharacterId():
                name = char_info.getName()

        self.private_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<b>{name}</b><b>HP:</b>{hp}<br><b>IP:</b>{ip}<br><b>Chips:</b>{chips}<br>",
            relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 2 * self.__icon_size),
                                      (self.__padding, self.__padding)),
            manager=self.manager,
            container=self.container,
            object_id="#private_textbox"
        )
