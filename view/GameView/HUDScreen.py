import logging
import traceback
import pygame_gui
import pygame
import cppyy

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.Visuals.VisualGadget import GADGET_NAME_LIST, GADGET_PATH_LIST
from view.GameView.Visuals.VisualProperty import PROPERTY_NAME_LIST, PROPERTY_PATH_LIST
from view.GameView.Visuals.VisualCharacter import CHAR_PATH_DICT
from view.GameView.HUDScreenElements.CharacterInfoBox import CharacterInfoBox
from view.GameView.HUDScreenElements.SelectionInfoBox import SelectionInfoBox
from view.GameView.HUDScreenElements.OperationStatusBox import OperationStatusBox
from view.GameView.HUDScreenElements.OperationLogBox import OperationLogBox
from controller.ControllerView import ControllerGameView
from network.NetworkEvent import NETWORK_EVENT

from cppyy.gbl.std import map, pair, set, vector

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/Point.hpp")
cppyy.include("datatypes/character/PropertyEnum.hpp")
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

    _valid_stake_inputs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

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

        self.character_info_box = CharacterInfoBox(self, self.container, self.manager)
        self.selection_info_box = SelectionInfoBox(self, self.container, self.manager, self.settings)
        self.operation_status_box = OperationStatusBox(self, self.container, self.manager, self.settings)
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

        logging.info("HudScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self._check_character_hover()
        self.selection_info_box.update_textbox(self.gadget_icon_list, self.property_icon_list,
                                               self.__selected_gad_prop_idx)

        self.window.blit(self.background, (0, self.container.rect.y))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)
        self.handle_shortcuts(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.menu_button: self.menu_button_pressed,
                self.send_action_button: self.send_action_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Element not found in dict")
        elif event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "GameStatus":
                self.network_update()
            elif event.message_type == "RequestGameOperation":
                self._update_active_char(active=True)
            elif event.message_type == "GamePause":
                self.selection_info_box.update_textbox(self.gadget_icon_list, self.property_icon_list,
                                                       self.__selected_gad_prop_idx)
        elif event.type == pygame.MOUSEBUTTONUP:
            # check if on one of the gadget / properties imgs
            for idx, icon in enumerate(self.gadget_icon_list + self.property_icon_list):
                if icon.check_hover(1 / self.settings.frame_rate, False):
                    self.__selected_gad_prop_idx = idx

    def menu_button_pressed(self) -> None:
        self.controller.to_main_menu()

    def send_action_pressed(self) -> bool:
        """
        Extract for action relevant information from GUI-Elements and call controller, which then calls the network
        todo: could return boolean if successfull
        :return:    None
        """
        ret = False
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
            stake_str = self.stake_entry_line.get_text()
            if stake_str == "":
                return False
            stake = int(stake_str)
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type, stake=stake)
            logging.info(f"Stake={stake}. Send Gamble Action successfull {ret}")
        elif type == "Property":
            # Observation = 0, BangAndBurn = 1
            prop = self.idx_to_property_idx(self.__selected_gad_prop_idx)
            logging.info(f"Property: {prop}")
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type, property=prop)
            logging.info(f"Send Property Action successfull: {ret}")
            # reset gadget / property selection
            self.__selected_gad_prop_idx = None
        elif type == "Gadget":
            # if selection is None, send action to pick up cocktail!
            gad = self.idx_to_gadget_idx(
                self.__selected_gad_prop_idx) if self.__selected_gad_prop_idx is not None else cppyy.gbl.spy.gadget.GadgetEnum.COCKTAIL
            target = self.parent.parent.get_selected_field()
            ret = self.controller.send_game_operation(target=target, op_type=type, gadget=gad)
            logging.info(f"Send Gadget Action successfull: {ret}")
            # reset gadget / property selection
            self.__selected_gad_prop_idx = None

        if ret:
            self._update_active_char(active=False)

        # update op. status box
        self.operation_status_box.update_valid_op(was_valid=ret)

        return ret

    def _check_character_hover(self) -> None:
        """
        Check if character image is currently hovered, if so init private textbox on this char
        :return:    None
        """
        self.character_info_box.reset()

        for idx, button in enumerate(self.char_image_list):
            if button.check_hover(1 / self.settings.frame_rate, False):
                self.character_info_box.update_textbox(idx)

    def network_update(self) -> None:
        """
        Interface to view. calls all internal methods needed to perform a network update step
        :return:    None
        """
        self._create_character_images()
        self._update_icons()
        self.operation_status_box.update_successfull_op()
        self.operation_log_box.update_textbox()

    def _update_icons(self) -> None:
        """
        Updates icons based on new network upate. Gets information from model and creates icon bar based on that
        :return:    None
        """
        # remove old gadgets
        for gad in self.gadget_icon_list:
            gad.kill()
        for prop in self.property_icon_list:
            prop.kill()
        self.gadget_icon_list.clear()
        self.property_icon_list.clear()

        my_chars = self.controller.lib_client_handler.lib_client.getChosenCharacters()
        count = 0

        for idx_char, char in enumerate(my_chars):
            char_gadgets = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char).getGadgets()

            for idx, gad in enumerate(char_gadgets):
                gad_idx = gad.getType()
                gad_icon_surface = pygame.image.load(GADGET_PATH_LIST[gad_idx])
                gad_icon_surface = pygame.transform.scale(gad_icon_surface, [self.__icon_size] * 2)

                self.gadget_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + idx * self.__icon_size, 0),
                        gad_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char + idx}"
                ))

                self.gadget_icon_list[count].normal_image = gad_icon_surface
                self.gadget_icon_list[count].hovered_image = gad_icon_surface
                self.gadget_icon_list[count].rebuild()
                count += 1

        count = 0
        for idx_char, char in enumerate(my_chars):
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char)
            # two executable properties
            hasObservation = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.OBSERVATION)
            hasBnB = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN)

            pos = 0
            if hasObservation:
                property_icon_surface = pygame.image.load(PROPERTY_PATH_LIST[0])
                property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

                self.property_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance), self.__icon_size),
                        property_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

                self.property_icon_list[count].normal_image = property_icon_surface
                self.property_icon_list[count].hovered_image = property_icon_surface
                self.property_icon_list[count].rebuild()
                pos += 1
                count += 1

            if hasBnB:
                property_icon_surface = pygame.image.load(PROPERTY_PATH_LIST[1])
                property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

                self.property_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + pos * self.__icon_size,
                         self.__icon_size),
                        property_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

                self.property_icon_list[count].normal_image = property_icon_surface
                self.property_icon_list[count].hovered_image = property_icon_surface
                self.property_icon_list[count].rebuild()
                count += 1

    def _create_character_images(self) -> None:
        """
        Gets information from model and creates character images based on that information
        :return:
        """
        self.char_image_list.clear()
        self.health_bar_list.clear()

        # test_surface to display images on character buttons
        char_surface = pygame.image.load(CHAR_PATH_DICT.get("normal")).convert_alpha()
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

    def _update_active_char(self, active) -> None:
        active_char_id = self.controller.lib_client_handler.lib_client.getActiveCharacter()
        active_gui_idx = 0

        for idx, char_id in enumerate(self.controller.lib_client_handler.lib_client.getChosenCharacters()):
            if char_id == active_char_id:
                active_gui_idx = idx

        key = "active" if active else "normal"

        active_img = pygame.image.load(CHAR_PATH_DICT.get(key))
        active_img = pygame.transform.scale(active_img, [int(self.__padding)] * 2)
        self.char_image_list[active_gui_idx].normal_image = active_img
        self.char_image_list[active_gui_idx].rebuild()

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

        self.stake_entry_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.container.rect.width - 2 * self.__distance - self.__button_size[0] - self.__status_textbox_width -
                 self.__dropdown_size[0], self.__dropdown_size[1]),
                self.__dropdown_size),
            manager=self.manager,
            container=self.container,
            object_id="#stake_entry_line"
        )

        self.stake_entry_line.set_text("1")
        self.stake_entry_line.allowed_characters = self._valid_stake_inputs

        self.stake_text_label = pygame_gui.elements.UILabel(
            text="Enter gambling stake",
            relative_rect=pygame.Rect(
                (self.container.rect.width - 2 * self.__distance - self.__button_size[0] - self.__status_textbox_width -
                 self.__dropdown_size[0], 0),
                self.__dropdown_size),
            manager=self.manager,
            container=self.container,
            object_id="#stake_text_label"
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

    def idx_to_gadget_idx(self, idx) -> int:
        """
        Transforms between idx for UI-elements list and State Gadget idx
        :param idx:     UI gadget idx
        :return:        State gadget idx
        """
        character_ids = self.controller.lib_client_handler.lib_client.getChosenCharacters()
        count = 0
        for char_id in character_ids:
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id)
            if idx - count < current_char.getGadgets().size():
                return current_char.getGadgets()[idx - count].getType()
            else:
                count += current_char.getGadgets().size()

    def idx_to_property_idx(self, idx) -> int:
        """
        Transforms between idx for UI-elements list and state property idx
        :param idx:     UI property idx
        :return:        State property idx
        """
        idx -= len(self.gadget_icon_list)

        character_ids = self.controller.lib_client_handler.lib_client.getChosenCharacters()
        count = 0

        for char_id in character_ids:
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id)

            hasObservation = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.OBSERVATION)
            hasBnB = current_char.hasProperty(cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN)

            count += int(hasObservation) + int(hasBnB)

            if count > idx:
                # found char
                if hasObservation and hasBnB:
                    return cppyy.gbl.spy.character.PropertyEnum.OBSERVATION if (count - 2) == idx \
                        else cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN
                else:
                    return cppyy.gbl.spy.character.PropertyEnum.OBSERVATION if hasObservation \
                        else cppyy.gbl.spy.character.PropertyEnum.BANG_AND_BURN

    @staticmethod
    def prop_idx_to_string(prop_idx) -> str:
        return "Observation" if prop_idx == cppyy.gbl.spy.character.PropertyEnum.OBSERVATION \
            else "Bang and Burn"

    def handle_shortcuts(self, event) -> None:
        if event.type != pygame.KEYUP:
            return

        if event.key == pygame.K_g:
            self.action_bar.selected_option = self.__actionbar_options[0]
        elif event.key == pygame.K_b:
            self.action_bar.selected_option = self.__actionbar_options[1]
        elif event.key == pygame.K_s:
            self.action_bar.selected_option = self.__actionbar_options[2]
        elif event.key == pygame.K_m:
            self.action_bar.selected_option = self.__actionbar_options[3]
        elif event.key == pygame.K_r:
            self.action_bar.selected_option = self.__actionbar_options[4]
        elif event.key == pygame.K_p:
            self.action_bar.selected_option = self.__actionbar_options[5]
        elif event.key == pygame.K_RETURN:
            self.send_action_pressed()

        self.action_bar.rebuild()
