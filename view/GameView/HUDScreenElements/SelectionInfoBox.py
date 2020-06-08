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
cppyy.include("datatypes/character/PropertyEnum.hpp")


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
                    if idx < len(gadget_icon_list):
                        # hovering gadget
                        gadget_idx = self.parent_screen.idx_to_gadget_idx(idx)
                        textbox_str += f"<b>Hovering Gadget:</b><br>{GADGET_NAME_LIST[gadget_idx]}<br>"
                    else:
                        # hovering property
                        property = self.parent_screen.idx_to_property_idx(idx)
                        property_str = "Observation" if property == cppyy.gbl.spy.character.PropertyEnum.OBSERVATION \
                            else "Bang and Burn"
                        textbox_str += f"<br>Hovering Property:<br>{property_str}"
                break

        if selected_gad_prop_idx is not None:
            if selected_gad_prop_idx < len(gadget_icon_list):
                # gadget selected
                gad = self.parent_screen.idx_to_gadget_idx(selected_gad_prop_idx)
                textbox_str += f"<b>Selected Gadget:</b><br>{GADGET_NAME_LIST[gad]}<br>"
                textbox_str += self._get_gadget_info(gad)
            else:
                # property selected
                property = self.parent_screen.idx_to_property_idx(selected_gad_prop_idx)
                property_str = "Observation" if property == cppyy.gbl.spy.character.PropertyEnum.OBSERVATION \
                    else "Bang and Burn"
                textbox_str += f"<br>Currently Selected:<br>{property_str}"

        if self.parent_screen.parent.parent.get_selected_field() is not None:
            # selected field information
            field = self.parent_screen.parent.parent.get_selected_field()
            # only update string, when selected field has changed
            if field != self.parent_screen.selected_field:
                self.parent_screen.selected_field = field
                textbox_str += f"<br>{self.__create_field_info_string(field)}<br>"
                update = True

        if self.parent_screen.controller.lib_client_handler.lib_client.isGamePaused():
            textbox_str += "<b>Game is paused!</b><br>"

        if update:
            self.info_textbox.html_text = textbox_str
            self.info_textbox.rebuild()
            self.__hovered_count = 0

    def __create_field_info_string(self, field) -> str:
        """
        Gets the selected field and creates a html string, to be displayed in the info box
        todo create state, so this is only done, when the selected field has changed
        :return:    formatted html-str
        """

        logging.info("Updating field info string")

        info_str = ""

        point_cpp = cppyy.gbl.spy.util.Point()
        point_cpp.x, point_cpp.y = field.x, field.y
        field_cpp = self.parent_screen.controller.lib_client_handler.lib_client.getState().getMap().getField(point_cpp)

        # get potential character standing on field
        characters = self.parent_screen.controller.lib_client_handler.lib_client.getState().getCharacters()
        char = cppyy.gbl.spy.util.GameLogicUtils.findInCharacterSetByCoordinates(characters, point_cpp)

        info = self.parent_screen.controller.lib_client_handler.lib_client.getInformation()
        variant = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)

        for char_info in char_info_vector:
            if char.getCharacterId() == char_info.getCharacterId():
                info_str += f"<b>Name:</b><br>{char_info.getName()}<br>"

        field_state = field_cpp.getFieldState()
        info_str += f"<b>Field state:</b><br>{FIELD_STATE_NAME_LIST[field_state]}<br><br>"

        if field_cpp.getGadget().has_value():
            gadget = field_cpp.getGadget().value().getType()
            info_str += f"<b>Gadget:</b><br>{GADGET_NAME_LIST[gadget]}<br>"
        if field_cpp.getChipAmount().has_value():
            chip_amount = field_cpp.getChipAmount().value()
            info_str += f"<b>Chip Amount:</b> {chip_amount}<br>"
        if field_cpp.isDestroyed().has_value():
            destroyed = field_cpp.isDestroyed().value()
            info_str += f"<b>Destroyed:</b> {destroyed}<br>"

        return info_str

    def _get_gadget_info(self, gadget_index) -> str:
        """
        Get info of selected gadget (usages left)
        :param gadget_index:
        :return:    formatted html-str
        """
        info_str = ""
        chosen_chars = self.parent_screen.controller.lib_client_handler.lib_client.getChosenCharacters()
        state = self.parent_screen.controller.lib_client_handler.lib_client.getState()

        for char_id in chosen_chars:
            char = state.getCharacters().findByUUID(char_id)
            gadget_opt = char.getGadget(cppyy.gbl.spy.gadget.GadgetEnum(gadget_index))
            if not gadget_opt.has_value():
                continue

            usages_left_opt = gadget_opt.value().getUsagesLeft()
            if usages_left_opt.has_value():
                info_str += f"<b>Usages left:</b> {usages_left_opt.value()}<br>"

        return info_str
