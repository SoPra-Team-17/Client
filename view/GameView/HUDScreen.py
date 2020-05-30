import logging
import traceback
import pygame_gui
import pygame
import cppyy

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.Visuals.VisualGadget import GADGET_NAME_LIST, GADGET_PATH_LIST
from controller.ControllerView import ControllerGameView
from network.NetworkEvent import NETWORK_EVENT

from cppyy.gbl.std import map, pair, set, vector

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/Point.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")


class HUDScreen(BasicView):
    __element_names = {"menu": "Menu", "send_action": "SendAction"}
    # starting option of dropdown
    __actionbar_starting_opt = "Select Action"
    __actionbar_options = ["Gadget", "Gamble", "Spy", "Movement", "Retire", "Property"]

    __status_textbox_width = 200
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    # size of gadget and property icons
    __icon_size = 32
    __button_size = (150, 35)
    __dropdown_size = (200, 35)
    # todo: hack find better solution
    __hovering_threshold = 15

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings,
                 parent: BasicView) -> None:
        super(HUDScreen, self).__init__(window, controller, settings)

        self.parent = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/HUDTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .0, self.settings.window_height * 3 / 4),
                                      (self.settings.window_width, self.settings.window_height / 4)),
            manager=self.manager
        )

        # padding to set responsive size of character buttons
        self.__padding = (self.container.rect.width / 2 - 5 * self.__distance) / 7
        self.font = pygame.font.Font("assets/GameView/Montserrat-Regular.ttf", 20)

        self.background = pygame.Surface((self.container.rect.width, self.container.rect.height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, "dark_bg"))

        self._init_ui_elements()

        self.__hovered_icon_idx = None
        self.__hovered_count = 0

        self.__selected_gad_prob_idx = None

        self.__selected_field = None
        self.__field_info_str = ""

        logging.info("HudScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self._check_character_hover()
        self._update_textbox()

        self.window.blit(self.background, (0, self.container.rect.y))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.menu_button: self.menu_button_pressed,
                self.send_action_button: self.send_action_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError as t:
                logging.error(traceback.format_exc())
                logging.warning("Element not found in dict")
        elif event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                self.network_update()
        elif event.type == pygame.MOUSEBUTTONUP:
            # check if on one of the gadget / properties imgs
            for idx, icon in enumerate(self.gadget_icon_list + self.property_icon_list):
                if icon.check_hover(1 / self.settings.frame_rate, False):
                    logging.info(f"Selected gad_prob_idx: {idx}")
                    self.__selected_gad_prob_idx = idx

    def menu_button_pressed(self) -> None:
        self.controller.to_main_menu()

    def send_action_pressed(self) -> None:
        logging.info(f"Selected Action: {self.action_bar.selected_option}")
        type = self.action_bar.selected_option
        if type == "Movement":
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type)
            logging.info(f"Send Movement successfull: {ret}")
        elif type == "Spy":
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type)
            logging.info(f"Send Spy Action successfull: {ret}")
        elif type == "Retire":
            ret = self.controller.send_game_operation(op_type=type)
            logging.info(f"Send Retire Action successfull: {ret}")
        elif type == "Gamble":
            # todo way needed to specify stake!
            stake = 1
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type, stake=stake)
            logging.info(f"Send Gamble Action successfull {ret}")
        elif type == "Property":
            # Observation = 0, BangAndBurn = 1
            prop = self.__selected_gad_prob_idx - len(self.gadget_icon_list)
            logging.info(f"Property: {prop}")
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type, property=prop)
            logging.info(f"Send Property Action successfull: {ret}")
            # reset gadget / property selection
            self.__selected_gad_prob_idx = None
        elif type == "Gadget":
            # if selection is None, send action to pick up cocktail!
            gad = self.__idx_to_gadget_idx(
                self.__selected_gad_prob_idx) if self.__selected_gad_prob_idx is not None else cppyy.gbl.spy.gadget.GadgetEnum.COCKTAIL
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type, gadget=gad)
            logging.info(f"Send Gadget Action successfull: {ret}")
            # reset gadget / property selection
            self.__selected_gad_prob_idx = None

    def _check_character_hover(self) -> None:
        # testing if character button idx is hovered, to show private_textbox
        # textbox is now recreated on each frame...
        # if the mouse is hovering over a character button and there is no private_textbox
        if self.private_textbox is not None:
            self.private_textbox.kill()
            self.private_textbox = None

        for idx, button in enumerate(self.char_image_list):
            if button.check_hover(1 / self.settings.frame_rate, False):
                self._init_private_textbox(idx)

    def _update_textbox(self) -> None:
        # check if any button is hovered --> update
        # todo improve performance of this method --> laggs when field on pf is selected
        update = False
        textbox_str = ""
        for idx, icon in enumerate(self.gadget_icon_list + self.property_icon_list):
            if icon.check_hover(1 / self.settings.frame_rate, False):
                if idx == self.__hovered_icon_idx:
                    self.__hovered_count += 1
                else:
                    self.__hovered_icon_idx = idx
                    continue

                if self.__hovered_count > self.__hovering_threshold:
                    update = True
                    if idx < len(self.gadget_icon_list):
                        # hovering gadget
                        gadget_idx = self.__idx_to_gadget_idx(idx)
                        textbox_str += f"Hovering Gadget:<br>{GADGET_NAME_LIST[gadget_idx]}"
                    else:
                        # hovering property
                        property = "Observation" if idx - len(self.gadget_icon_list) == 0 else "Bang and Burn"
                        textbox_str += f"Hovering Property:<br>{property}"
                break

        if self.__selected_gad_prob_idx is not None:
            if self.__selected_gad_prob_idx < len(self.gadget_icon_list):
                # gadget selected
                gad = self.__idx_to_gadget_idx(self.__selected_gad_prob_idx)
                textbox_str += f"<br>Currently Selected:<br>{GADGET_NAME_LIST[gad]}"
            else:
                # property selected
                property = "Observation" if self.__selected_gad_prob_idx - len(
                    self.gadget_icon_list) == 0 else "Bang and Burn"
                textbox_str += f"<br>Currently Selected:<br>{property}"

        if self.parent.parent.get_selected_field() is not None:
            # selected field information
            field = self.parent.parent.get_selected_field()
            # only update string, when selected field has changed
            if field != self.__selected_field:
                self.__selected_field = field
                self.__create_field_info_string(field)
                textbox_str += f"<br>Field: {self.__field_info_str}"
                update = True

        if update:
            self.info_textbox.html_text = textbox_str
            self.info_textbox.rebuild()
            self.__hovered_count = 0

    def network_update(self):
        logging.info("Performing HUD network update")
        self._create_character_images()
        self._update_icons()

    def _update_icons(self) -> None:
        self.gadget_icon_list.clear()
        self.property_icon_list.clear()

        gadget_icon_surface = pygame.image.load("assets/GameView/axe.png")
        gadget_icon_surface = pygame.transform.scale(gadget_icon_surface, [self.__icon_size] * 2)

        property_icon_surface = pygame.image.load("assets/GameView/ClammyClothes.png")
        property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

        my_chars = self.controller.lib_client_handler.lib_client.getChosenCharacters()

        for idx_char, char in enumerate(my_chars):
            char_gadgets = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char).getGadgets()

            # todo display correct gadget
            for idx in range(char_gadgets.size()):
                self.gadget_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + idx * self.__icon_size, 0),
                        gadget_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

        for idx_char, char in enumerate(my_chars):
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char)
            # two executable properties
            hasObservation = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.OBSERVATION)
            hasBnB = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN)

            # todo display correct property
            if hasObservation:
                self.property_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + self.__icon_size, self.__icon_size),
                        gadget_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

            if hasBnB:
                self.property_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + int(hasObservation) * self.__icon_size,
                         self.__icon_size),
                        gadget_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

        for gad in self.gadget_icon_list:
            gad.normal_image = gadget_icon_surface
            gad.rebuild()

        for prop in self.property_icon_list:
            prop.normal_image = property_icon_surface
            prop.rebuild()

    def _create_character_images(self) -> None:
        self.char_image_list.clear()
        self.health_bar_list.clear()

        # test_surface to display images on character buttons
        char_surface = pygame.image.load("assets/GameView/trash.png").convert_alpha()
        char_surface = pygame.transform.scale(char_surface, (int(self.__padding), int(self.__padding)))

        my_chars = self.controller.lib_client_handler.lib_client.getChosenCharacters()
        my_gadgets = self.controller.lib_client_handler.lib_client.getChosenGadgets()

        ip_sum = 0

        for idx, char in enumerate(my_chars):
            self.char_image_list.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 2 * self.__icon_size),
                                              char_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image0{idx}"
                )
            )

            self.health_bar_list.append(
                pygame_gui.elements.UIScreenSpaceHealthBar(
                    relative_rect=pygame.Rect(
                        (idx * (self.__padding + self.__distance),
                         self.__padding + self.__distance + 2 * self.__icon_size),
                        (self.__padding, 25)),
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#health_bar0{idx}",
                )
            )
            # get hp of char
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char)
            current_char_hp = current_char.getHealthPoints()
            ip_sum += current_char.getIntelligencePoints()

            self.health_bar_list[idx].current_health = current_char_hp
            self.health_bar_list[idx].health_percentag = current_char_hp / 100
            self.health_bar_list[idx].rebuild()

        # textbox has to be recreated, to reparse html text anyway..
        if self.status_textbox is not None:
            self.status_textbox.kill()

        active_char = self.controller.lib_client_handler.lib_client.getActiveCharacter()
        mp = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            active_char).getMovePoints()
        ap = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
            active_char).getActionPoints()

        self.status_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<strong>Intelligence Points:</strong>{ip_sum}<br><br><strong>Movement Points:</strong>{mp}<br><br>" \
                      f"<strong>Action Points:</strong>{ap}<br>",
            relative_rect=pygame.Rect(
                (len(self.char_image_list) * (self.__padding + self.__distance), 0),
                (self.__status_textbox_width, self.container.get_rect().height)),
            manager=self.manager,
            container=self.container,
            object_id="#status_textbox"
        )

        # loading sample image on character buttons
        for char in self.char_image_list:
            char.normal_image = char_surface
            char.rebuild()

    def _init_ui_elements(self) -> None:
        self.char_image_list = []
        self.health_bar_list = []
        self.private_textbox = None
        self.status_textbox = None

        self.gadget_icon_list = []
        self.property_icon_list = []

        # implementing a dropdown action_bar with all actions a character can perform
        self.action_bar = pygame_gui.elements.UIDropDownMenu(
            options_list=self.__actionbar_options,
            starting_option=self.__actionbar_starting_opt,
            relative_rect=pygame.Rect(
                (self.container.rect.width - 2 * self.__distance - self.__button_size[0] - self.__status_textbox_width -
                 self.__dropdown_size[0], self.container.rect.height - self.__dropdown_size[1]),
                self.__dropdown_size),
            manager=self.manager,
            container=self.container,
            object_id="#action_bar",
        )

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__button_size[0], self.container.rect.height - self.__button_size[1]),
                (self.__button_size)),
            text=self.__element_names["menu"],
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )

        self.send_action_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.width - self.__button_size[0],
                                       self.container.rect.height - 2 * self.__button_size[1] - self.__distance),
                                      (self.__button_size)),
            text=self.__element_names["send_action"],
            manager=self.manager,
            container=self.container,
            object_id="#send_action"

        )

        self.info_textbox = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__button_size[0] - self.__distance - self.__info_textbox_width, 0),
                (self.__info_textbox_width, self.container.rect.height)),
            manager=self.manager,
            container=self.container,
            object_id="info_textbox"
        )


    def _init_private_textbox(self, idx) -> None:
        # todo properly format
        char_id = self.controller.lib_client_handler.lib_client.getChosenCharacters()[idx]
        char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(char_id)

        hp = char.getHealthPoints()
        chips = char.getChips()
        ip = char.getIntelligencePoints()
        info = self.controller.lib_client_handler.lib_client.getInformation()
        variant = info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION]
        char_info_vector = cppyy.gbl.std.get[vector[cppyy.gbl.spy.character.CharacterInformation]](variant)

        chosen_char_id = self.controller.lib_client_handler.lib_client.getChosenCharacters()[idx]
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

    def __idx_to_gadget_idx(self, idx):
        """
        Transforms between idx for UI-elements list and State Gadget idx
        :param idx:     UI gadget idx
        :return:        State gadget idx
        """
        character_ids = self.controller.lib_client_handler.lib_client.getChosenCharacters()
        count = 0
        for char_id in character_ids:
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(char_id)
            if idx - count < current_char.getGadgets().size():
                return current_char.getGadgets()[idx - count].getType()
            else:
                count += current_char.getGadgets().size()

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
        field_cpp = self.controller.lib_client_handler.lib_client.getState().getMap().getField(point_cpp)
        # todo extract all relevant information from field and format to string
        # todo get potential character standing on field! and display name and of own faction!
        foggy = field_cpp.isFoggy()
        info_str += f"Is Foggy: {foggy}<br>"
        if field_cpp.getGadget().has_value():
            gadget = field_cpp.getGadget().value().getType()
            info_str += f"Gadget: {GADGET_NAME_LIST[gadget]}<br>"
        if field_cpp.getChipAmount().has_value():
            chip_amount = field_cpp.getChipAmount().value()
            info_str += f"Chip Amount: {chip_amount}<br>"
        if field_cpp.getSafeIndex().has_value():
            safe_index = field_cpp.getSafeIndex().value()
            info_str += f"Safe Index: {safe_index}<br>"
        if field_cpp.isDestroyed().has_value():
            destroyed = field_cpp.isDestroyed().value()
            info_str += f"Is Destroyed: {destroyed}<br>"

        self.__field_info_str = info_str
