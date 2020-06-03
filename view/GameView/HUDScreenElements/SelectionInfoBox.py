"""
Implements the selection info box, which displays information about the selected field and gadget / property
"""
import logging
import pygame_gui
import pygame
import cppyy

from view.GameView.Visuals.VisualGadget import GADGET_NAME_LIST, GADGET_PATH_LIST
from view.GameView.Visuals.VisualFieldState import FIELD_STATE_NAME_LIST
from view.ViewSettings import ViewSettings

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
cppyy.include("util/GameLogicUtils.hpp")


class SelectionInfoBox:
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    __button_size = (150, 35)
    # todo: hack find better solution
    __hovering_threshold = 15

    def __init__(self, parent, container: pygame_gui.core.UIContainer, manager: pygame_gui.UIManager,
                 settings: ViewSettings):
        self.parent_screen = parent
        self.container = container
        self.manager = manager
        self.settings = settings

        self.__hovered_count = 0
        self.__field_info_str = ""

        self.info_textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__button_size[0] - self.__distance - self.__info_textbox_width, 0),
                (self.__info_textbox_width, self.container.rect.height)),
            manager=self.manager,
            container=self.container,
            object_id="info_textbox"
        )

    def update_textbox(self, gadget_icon_list, property_icon_list, selected_gad_prop_idx) -> None:
        """
        Interface to parent screen, to update textbox
        :return:    None
        """
        self._update_textbox(gadget_icon_list, property_icon_list, selected_gad_prop_idx)

    def _update_textbox(self, gadget_icon_list, property_icon_list, selected_gad_prop_idx) -> None:
        """
        Updates text inside textbox
        todo improve performance of this method --> laggs when field on pf is selected
        :return:    None
        """
        # check if any button is hovered --> update
        update = False
        textbox_str = ""
        for idx, icon in enumerate(gadget_icon_list + property_icon_list):
            if icon.check_hover(1 / self.settings.frame_rate, False):
                if idx == self.parent_screen.hovered_icon_idx:
                    self.__hovered_count += 1
                else:
                    self.parent_screen.hovered_icon_idx = idx
                    continue

                if self.__hovered_count > self.__hovering_threshold:
                    update = True
                    logging.info("Should update gad/prop")
                    if idx < len(gadget_icon_list):
                        # hovering gadget
                        gadget_idx = self.parent_screen.idx_to_gadget_idx(idx)
                        textbox_str += f"Hovering Gadget:<br>{GADGET_NAME_LIST[gadget_idx]}"
                    else:
                        # hovering property
                        property = "Observation" if idx - len(gadget_icon_list) == 0 else "Bang and Burn"
                        textbox_str += f"Hovering Property:<br>{property}"
                break

        if selected_gad_prop_idx is not None:
            if selected_gad_prop_idx < len(gadget_icon_list):
                # gadget selected
                gad = self.parent_screen.idx_to_gadget_idx(selected_gad_prop_idx)
                textbox_str += f"<br>Currently Selected:<br>{GADGET_NAME_LIST[gad]}"
            else:
                # property selected
                property = "Observation" if selected_gad_prop_idx - len(
                    gadget_icon_list) == 0 else "Bang and Burn"
                textbox_str += f"<br>Currently Selected:<br>{property}"

        if self.parent_screen.parent.parent.get_selected_field() is not None:
            # selected field information
            field = self.parent_screen.parent.parent.get_selected_field()
            # only update string, when selected field has changed
            if field != self.parent_screen.selected_field:
                self.parent_screen.selected_field = field
                self.__create_field_info_string(field)
                textbox_str += f"<br>Field: {self.__field_info_str}"
                update = True

        if update:
            self.info_textbox.html_text = textbox_str
            self.info_textbox.rebuild()
            self.__hovered_count = 0

    def __create_field_info_string(self, field) -> None:
        """
        Gets the selected field and creates a html string, to be displayed in the info box
        todo create state, so this is only done, when the selected field has changed
        :return:
        """

        logging.info("Updating field info string")

        info_str = ""

        point_cpp = cppyy.gbl.spy.util.Point()
        point_cpp.x, point_cpp.y = field.x, field.y
        field_cpp = self.parent_screen.controller.lib_client_handler.lib_client.getState().getMap().getField(point_cpp)

        field_state = field_cpp.getFieldState()
        info_str += f"Field state: <b>{FIELD_STATE_NAME_LIST[field_state]}</b><br>"

        foggy = field_cpp.isFoggy()
        info_str += f"Is Foggy: {foggy}<br>"

        if field_cpp.getGadget().has_value():
            gadget = field_cpp.getGadget().value().getType()
            info_str += f"Gadget: {GADGET_NAME_LIST[gadget]}<br>"
        if field_cpp.getChipAmount().has_value():
            chip_amount = field_cpp.getChipAmount().value()
            info_str += f"Chip Amount: {chip_amount}<br>"
        if field_cpp.isDestroyed().has_value():
            destroyed = field_cpp.isDestroyed().value()
            info_str += f"Is Destroyed: {destroyed}<br>"

        # get potential character standing on field
        characters = self.parent_screen.controller.lib_client_handler.lib_client.getState().getCharacters()
        char = cppyy.gbl.spy.util.GameLogicUtils.findInCharacterSetByCoordinates(characters, point_cpp)

        info = self.parent_screen.controller.lib_client_handler.lib_client.getInformation()
        variant = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)

        for char_info in char_info_vector:
            if char.getCharacterId() == char_info.getCharacterId():
                info_str += f"Char. name: <b>{char_info.getName()}</b><br>"

        self.__field_info_str = info_str
