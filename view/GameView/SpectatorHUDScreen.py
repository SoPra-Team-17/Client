"""
Implements HUD for spectator
"""
import logging
import pygame
import pygame_gui
import cppyy

from cppyy.gbl.std import vector

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.Visuals.VisualGadget import GADGET_PATH_LIST
from view.GameView.Visuals.VisualProperty import PROPERTY_PATH_LIST
from view.GameView.Visuals.VisualCharacter import CHAR_PATH_DICT
from view.GameView.HUDScreenElements.SelectionInfoBox import SelectionInfoBox
from view.GameView.HUDScreenElements.OperationLogBox import OperationLogBox
from controller.ControllerView import ControllerSpectatorView
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "11.06.2020 (doc. creation)"

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/Point.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")
cppyy.include("datatypes/character/PropertyEnum.hpp")


class SpectatorHUDScreen(BasicView):
    __element_names = {"menu": "Menu"}
    __status_textbox_width = 200
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    # size of gadget and property icons
    __icon_size = 32
    __button_size = (200, 35)
    __dropdown_size = (200, 35)

    def __init__(self, window: pygame.display, controller: ControllerSpectatorView, parent,
                 settings: ViewSettings) -> None:
        super(SpectatorHUDScreen, self).__init__(window, controller, settings)

        self.parent = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/HUDTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .0, self.settings.window_height * 3 / 4),
                                      (self.settings.window_width, self.settings.window_height / 4)),
            manager=self.manager
        )

        self.operation_log_box = OperationLogBox(self, self.container, self.manager, self.settings)

        # padding to set responsive size of character buttons
        self.__padding = (self.container.rect.width / 2 - 5 * self.__distance) / 7
        self.font = pygame.font.Font("assets/GameView/Montserrat-Regular.ttf", 20)

        self.background = pygame.Surface((self.container.rect.width, self.container.rect.height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, "dark_bg"))

        self._init_ui_elements()

        self.hovered_icon_idx = None

        self.__selected_gad_prop_idx = None

        self.selected_field = None
        self.private_textbox = None

        logging.info("HudScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)
        self._update_text_box()
        self._check_character_hover()

        self.window.blit(self.background, (0, self.container.rect.y))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.menu_button: self.menu_button_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Element not found in dict")
        elif event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                self.network_update()

    def menu_button_pressed(self) -> None:
        self.parent.to_settings()

    def _check_character_hover(self) -> None:
        """
        Check if character image is currently hovered, if so init private textbox on this char
        :return:    None
        """
        if self.private_textbox is not None:
            self.private_textbox.kill()
            self.private_textbox = None

        for idx, button in enumerate(self.char_image_list_p1):
            if button.check_hover(1 / self.settings.frame_rate, False):
                # self.character_info_box.update_textbox(idx)
                self._update_character_info_box(idx, player_one=True)
                return

        for idx, button in enumerate(self.char_image_list_p2):
            if button.check_hover(1 / self.settings.frame_rate, False):
                self._update_character_info_box(idx, player_one=False)
                return

    def network_update(self) -> None:
        """
        Interface to view. calls all internal methods needed to perform a network update
        :return:    None
        """
        self._create_character_images()
        self._update_icons()
        self.operation_log_box.update_textbox()

    def _create_character_images(self) -> None:
        """
        Gets information from model and creates character images based on that information
        :return:    None
        """
        self.char_image_list_p1.clear()
        self.char_image_list_p2.clear()

        char_surface_normal = pygame.image.load(CHAR_PATH_DICT.get("normal")).convert_alpha()
        char_surface_normal = pygame.transform.scale(char_surface_normal, (int(self.__padding), int(self.__padding)))

        player_one_id = self.controller.lib_client_handler.lib_client.getMyFactionList()
        for idx, char_id in enumerate(player_one_id):
            self.char_image_list_p1.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 3 * self.__icon_size),
                                              char_surface_normal.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image_p1_0{idx}"
                )
            )

            self.char_image_list_p1[idx].normal_image = char_surface_normal
            self.char_image_list_p1[idx].rebuild()

        player_two_id = self.controller.lib_client_handler.lib_client.getEnemyFactionList()
        for idx, char_id in enumerate(player_two_id):
            self.char_image_list_p2.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - (idx + 1) * (self.__padding + self.__distance),
                         3 * self.__icon_size),
                        char_surface_normal.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image_p1_0{idx}"
                )
            )

            self.char_image_list_p2[idx].normal_image = char_surface_normal
            self.char_image_list_p2[idx].rebuild()

    def _update_icons(self) -> None:
        """
        Updates icons based on new network update. Gets information from model and creates icon bar based on that
        :return:    None
        """
        # remove old gadgets
        for gad in self.gadget_icon_list_p1 + self.gadget_icon_list_p2:
            gad.kill()
        for prop in self.property_icon_list_p1 + self.property_icon_list_p2:
            prop.kill()

        self.gadget_icon_list_p1.clear()
        self.gadget_icon_list_p2.clear()
        self.property_icon_list_p1.clear()
        self.property_icon_list_p2.clear()

        count = 0
        player_one_id = self.controller.lib_client_handler.lib_client.getMyFactionList()
        for idx_char, char_id in enumerate(player_one_id):
            char_gadgets = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id).getGadgets()

            for idx, gad in enumerate(char_gadgets):
                gad_idx = gad.getType()
                gad_icon_surface = pygame.image.load(GADGET_PATH_LIST[gad_idx])
                gad_icon_surface = pygame.transform.scale(gad_icon_surface, [self.__icon_size] * 2)

                x_pos = idx * self.__icon_size
                y_pos = 0
                if idx >= 4:
                    x_pos = (idx - 4) * self.__icon_size
                    y_pos = self.__icon_size
                if idx >= 8:
                    # leave space for 2 props
                    x_pos = (idx - 6) * self.__icon_size
                    y_pos = 2 * self.__icon_size

                self.gadget_icon_list_p1.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + x_pos, y_pos),
                        gad_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char + idx}"
                ))
                self.gadget_icon_list_p1[count].normal_image = gad_icon_surface
                self.gadget_icon_list_p1[count].hovered_image = gad_icon_surface
                self.gadget_icon_list_p1[count].rebuild()
                count += 1

        count = 0
        for idx_char, char_id in enumerate(player_one_id):
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id)
            # two executable properties
            hasObservation = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.OBSERVATION)
            hasBnB = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN)

            pos = 0
            if hasObservation:
                property_icon_surface = pygame.image.load(PROPERTY_PATH_LIST[0])
                property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

                self.property_icon_list_p1.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance), 2 * self.__icon_size),
                        property_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

                self.property_icon_list_p1[count].normal_image = property_icon_surface
                self.property_icon_list_p1[count].hovered_image = property_icon_surface
                self.property_icon_list_p1[count].rebuild()
                pos += 1
                count += 1

            if hasBnB:
                property_icon_surface = pygame.image.load(PROPERTY_PATH_LIST[1])
                property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

                self.property_icon_list_p1.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + pos * self.__icon_size,
                         2 * self.__icon_size),
                        property_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

                self.property_icon_list_p1[count].normal_image = property_icon_surface
                self.property_icon_list_p1[count].hovered_image = property_icon_surface
                self.property_icon_list_p1[count].rebuild()
                count += 1

        count = 0
        player_two_id = self.controller.lib_client_handler.lib_client.getEnemyFactionList()
        for idx_char, char_id in enumerate(player_two_id):
            char_gadgets = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id).getGadgets()

            for idx, gad in enumerate(char_gadgets):
                gad_idx = gad.getType()
                gad_icon_surface = pygame.image.load(GADGET_PATH_LIST[gad_idx])
                gad_icon_surface = pygame.transform.scale(gad_icon_surface, [self.__icon_size] * 2)

                x_pos = idx * self.__icon_size
                y_pos = 0

                if idx >= 4:
                    x_pos = (idx - 4) * self.__icon_size
                    y_pos = self.__icon_size
                if idx >= 8:
                    # leave space for two props
                    x_pos = (idx - 6) * self.__icon_size
                    y_pos = 2 * self.__icon_size

                self.gadget_icon_list_p2.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - (idx_char + 1) * (
                                self.__padding + self.__distance) + x_pos,
                         y_pos),
                        gad_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char + idx}"
                ))

                self.gadget_icon_list_p2[count].normal_image = gad_icon_surface
                self.gadget_icon_list_p2[count].hovered_image = gad_icon_surface
                self.gadget_icon_list_p2[count].rebuild()
                count += 1

        count = 0
        for idx_char, char_id in enumerate(player_two_id):
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id)
            # two executable properties
            hasObservation = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.OBSERVATION)
            hasBnB = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN)

            pos = 0
            if hasObservation:
                property_icon_surface = pygame.image.load(PROPERTY_PATH_LIST[0])
                property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

                self.property_icon_list_p2.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - idx_char * (self.__padding + self.__distance),
                         2 * self.__icon_size),
                        property_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

                self.property_icon_list_p2[count].normal_image = property_icon_surface
                self.property_icon_list_p2[count].hovered_image = property_icon_surface
                self.property_icon_list_p2[count].rebuild()
                pos += 1
                count += 1

            if hasBnB:
                property_icon_surface = pygame.image.load(PROPERTY_PATH_LIST[1])
                property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

                self.property_icon_list_p2.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - idx_char * (
                                self.__padding + self.__distance) + pos * self.__icon_size,
                         2 * self.__icon_size),
                        property_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

                self.property_icon_list_p2[count].normal_image = property_icon_surface
                self.property_icon_list_p2[count].hovered_image = property_icon_surface
                self.property_icon_list_p2[count].rebuild()
                count += 1

    def _init_ui_elements(self):
        self.char_image_list_p1 = []
        self.char_image_list_p2 = []
        self.private_textbox = None
        self.status_textbox = None

        self.gadget_icon_list_p1 = []
        self.gadget_icon_list_p2 = []
        self.property_icon_list_p1 = []
        self.property_icon_list_p2 = []

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.operation_log_box.textbox.rect.x - self.__button_size[0] - 25,
                 self.container.rect.height - self.__button_size[1]),
                (self.__button_size)),
            text=self.__element_names["menu"],
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )

        self.selected_info_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                (self.operation_log_box.textbox.rect.x - self.__button_size[0] - 25,
                 0),
                (self.__button_size[0], self.container.rect.height - self.__button_size[1])),
            html_text="",
            manager=self.manager,
            container=self.container,
            object_id="#selected_info_box"
        )

    def _update_text_box(self) -> None:
        update = False
        textbox_str = ""

        if self.parent.get_selected_field() is not None:
            # selected field information
            field = self.parent.get_selected_field()
            # only update string, when selected field has changed
            if field != self.selected_field:
                self.selected_field = field
                info_str = SelectionInfoBox.create_field_info_string(self.controller, field)
                textbox_str += f"<br>Field: {info_str}"
                update = True

        if update:
            self.selected_info_box.html_text = textbox_str
            self.selected_info_box.rebuild()

    def _update_character_info_box(self, idx: int, player_one: bool) -> None:
        # todo bc libclient switched from vector to set
        char_id = None
        char_list = self.controller.lib_client_handler.lib_client.getMyFactionList() if player_one \
            else self.controller.lib_client_handler.lib_client.getEnemyFactionList()
        for it, c_id in enumerate(char_list):
            if it == idx:
                char_id = c_id

        char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(char_id)

        hp = char.getHealthPoints()
        chips = char.getChips()
        ip = char.getIntelligencePoints()
        info = self.controller.lib_client_handler.lib_client.getInformation()
        variant = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)

        name = ""
        for char_info in char_info_vector:
            if char_id == char_info.getCharacterId():
                name = char_info.getName()

        html_str = f"<b>{name}</b><br><b>HP:</b>{hp}<br><b>IP:</b>{ip}<br><b>Chips:</b>{chips}<br>"

        has_clammy_clothes = char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.CLAMMY_CLOTHES)
        if has_clammy_clothes:
            html_str += f"<br>Has clammy clothes"

        if player_one:
            self.private_textbox = pygame_gui.elements.UITextBox(
                html_text=html_str,
                relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 0),
                                          (self.__padding, self.__padding + 3 * self.__icon_size)),
                manager=self.manager,
                container=self.container,
                object_id="#private_textbox"
            )
        else:
            self.private_textbox = pygame_gui.elements.UITextBox(
                html_text=html_str,
                relative_rect=pygame.Rect((self.container.rect.width - (idx + 1) * (self.__padding + self.__distance),
                                           0),
                                          (self.__padding, self.__padding + 3 * self.__icon_size)),
                manager=self.manager,
                container=self.container,
                object_id="#private_textbox"
            )
