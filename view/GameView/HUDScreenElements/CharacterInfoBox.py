"""
Implements character info box which displays information about the character (e.g. name, chips, ip, etc.)
"""
import pygame_gui
import pygame
import cppyy

from cppyy.gbl.std import vector

__author__ = "Marco Deuscher"
__date__ = "02.06.20 (creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")
cppyy.include("datatypes/character/PropertyEnum.hpp")


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
        # todo dirty hack, because libclient switched to set!
        char_id = None
        for it, c_id in enumerate(self.parent_screen.controller.lib_client_handler.lib_client.getMyFactionList()):
            if idx == it:
                char_id = c_id
        # char_id = self.parent_screen.controller.lib_client_handler.lib_client.getMyFactionList()[idx]
        char = self.parent_screen.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            char_id)

        hp = char.getHealthPoints()
        chips = char.getChips()
        ip = char.getIntelligencePoints()
        info = self.parent_screen.controller.lib_client_handler.lib_client.getInformation()
        variant = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)

        has_clammy_clothes = char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.CLAMMY_CLOTHES)

        name = ""
        for char_info in char_info_vector:
            if char_id == char_info.getCharacterId():
                name = char_info.getName()

        html_str = f"<b>{name}</b><br><b>HP:</b>{hp}<br><b>IP:</b>{ip}<br><b>Chips:</b>{chips}<br>"

        if has_clammy_clothes:
            html_str += f"<br>Has clammy clothes"

        self.private_textbox = pygame_gui.elements.UITextBox(
            html_text=html_str,
            relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 0),
                                      (self.__padding, 3 * self.__icon_size + self.__padding)),
            manager=self.manager,
            container=self.container,
            object_id="#private_textbox"
        )
