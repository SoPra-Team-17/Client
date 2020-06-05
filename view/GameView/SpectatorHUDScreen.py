"""
Implements HUD for spectator
"""
import logging
import pygame
import pygame_gui
import cppyy

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.Visuals.VisualGadget import GADGET_PATH_LIST, GADGET_NAME_LIST
from view.GameView.Visuals.VisualProperty import PROPERTY_PATH_LIST, PROPERTY_NAME_LIST
from view.GameView.Visuals.VisualCharacter import CHAR_PATH_DICT
from view.GameView.HUDScreenElements.CharacterInfoBox import CharacterInfoBox
from view.GameView.HUDScreenElements.SelectionInfoBox import SelectionInfoBox
from controller.ControllerView import ControllerSpectatorView
from network.NetworkEvent import NETWORK_EVENT

from cppyy.gbl.std import map, pair, set, vector

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("util/Point.hpp")
cppyy.include("datatypes/gadgets/GadgetEnum.hpp")
cppyy.include("datatypes/character/CharacterInformation.hpp")
cppyy.include("network/messages/MetaInformationKey.hpp")


class SpectatorHUDScreen(BasicView):
    __element_names = {"menu": "Menu"}
    __status_textbox_width = 200
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    # size of gadget and property icons
    __icon_size = 32
    __button_size = (150, 35)
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

        self.character_info_box = CharacterInfoBox(self, self.container, self.manager)
        self.selection_info_box = SelectionInfoBox(self, self.container, self.manager, self.settings)

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
        elif event.type == pygame.MOUSEBUTTONUP:
            # check if on one of the gadget / properties imgs
            for idx, icon in enumerate(self.gadget_icon_list + self.property_icon_list):
                if icon.check_hover(1 / self.settings.frame_rate, False):
                    logging.info(f"Selected gad_prob_idx: {idx}")
                    self.__selected_gad_prop_idx = idx

    def menu_button_pressed(self) -> None:
        self.controller.to_main_menu()

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
        Interface to view. calls all internal methods needed to perform a network update
        :return:    None
        """
        self._create_character_images()
        self._update_icons()

    def _create_character_images(self) -> None:
        """
        Gets information from model and creates character images based on that information
        :return:    None
        """
        self.char_image_list_p1.clear()
        self.char_image_list_p2.clear()

        char_surface = pygame.image.load(CHAR_PATH_DICT.get("normal")).convert_alpha()
        char_surface = pygame.transform.scale(char_surface, (int(self.__padding), int(self.__padding)))

        for idx, char_id in enumerate(self.parent.player_one_id):
            self.char_image_list_p1.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 2 * self.__icon_size),
                                              char_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image_p1_0{idx}"
                )
            )

            self.health_bar_list_p1.append(
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
                char_id)
            current_char_hp = current_char.getHealthPoints()

            self.health_bar_list_p1[idx].current_health = current_char_hp
            self.health_bar_list_p1[idx].health_percentag = current_char_hp / 100
            self.health_bar_list_p1[idx].rebuild()

        for idx, char_id in enumerate(self.parent.player_two_id):
            self.char_image_list_p2.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - (idx + 1) * (self.__padding + self.__distance),
                         2 * self.__icon_size),
                        char_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image_p1_0{idx}"
                )
            )

            self.health_bar_list_p2.append(
                pygame_gui.elements.UIScreenSpaceHealthBar(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - (idx + 1) * (self.__padding + self.__distance),
                         2 * self.__icon_size),
                        char_surface.get_size()),
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#health_bar0{idx}",
                )
            )

            # get hp of char
            current_char = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id)
            current_char_hp = current_char.getHealthPoints()

            self.health_bar_list_p2[idx].current_health = current_char_hp
            self.health_bar_list_p2[idx].health_percentag = current_char_hp / 100
            self.health_bar_list_p2[idx].rebuild()

    def _update_icons(self) -> None:
        """
        Updates icons based on new network update. Gets information from model and creates icon bar based on that
        :return:    None
        """
        # remove old gadgets
        for gad in (self.gadget_icon_list_p1 + self.gadget_icon_list_p2):
            gad.kill()
        for prop in (self.property_icon_list_p1 + self.property_icon_list_p2):
            prop.kill()

        self.gadget_icon_list_p1.clear()
        self.gadget_icon_list_p2.clear()
        self.property_icon_list_p1.clear()
        self.property_icon_list_p2.clear()

        count = 0
        for idx_char, char_id in enumerate(self.parent.player_one_id):
            char_gadgets = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id).getGadgets()

            for idx, gad in enumerate(char_gadgets):
                gad_idx = gad.getType()
                gad_icon_surface = pygame.image.load(GADGET_PATH_LIST[gad_idx])
                gad_icon_surface = pygame.transform.scale(gad_icon_surface, [self.__icon_size] * 2)

                self.gadget_icon_list_p1.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + idx * self.__icon_size, 0),
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
        for idx_char, char_id in enumerate(self.parent.player_one_id):
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
                        (idx_char * (self.__padding + self.__distance), self.__icon_size),
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
                         self.__icon_size),
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
        for idx_char, char_id in enumerate(self.parent.player_two_id):
            char_gadgets = self.controller.lib_client_handler.lib_client.getState().getCharacters().findByUUID(
                char_id).getGadgets()

            for idx, gad in enumerate(char_gadgets):
                gad_idx = gad.getType()
                gad_icon_surface = pygame.image.load(GADGET_PATH_LIST[gad_idx])
                gad_icon_surface = pygame.transform.scale(gad_icon_surface, [self.__icon_size] * 2)

                self.gadget_icon_list_p2.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (self.container.rect.width - (idx_char + 1) * (
                                self.__padding + self.__distance) + idx * self.__icon_size,
                         0),
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
        for idx_char, char_id in enumerate(self.parent.player_two_id):
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
                        (self.container.rect.width - idx_char * (self.__padding + self.__distance), self.__icon_size),
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
                        (self.container.rect.width - idx_char * (
                                self.__padding + self.__distance) + pos * self.__icon_size,
                         self.__icon_size),
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

    def _init_ui_elements(self):
        self.char_image_list_p1 = []
        self.health_bar_list_p1 = []
        self.health_bar_list_p2 = []
        self.char_image_list_p2 = []
        self.private_textbox = None
        self.status_textbox = None

        self.gadget_icon_list_p1 = []
        self.gadget_icon_list_p2 = []
        self.property_icon_list_p1 = []
        self.property_icon_list_p2 = []

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.container.rect.width / 2 - self.__button_size[0] / 2,
                 self.container.rect.height - self.__button_size[1]),
                (self.__button_size)),
            text=self.__element_names["menu"],
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )

    def idx_to_gadget_idx(self, idx) -> int:
        """
        Transforms between idx for UI-elements list and State Gadget idx
        todo modify for both lists!
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
