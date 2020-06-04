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
            elif event.message_type == "RequestGameOperation":
                self._update_active_char(active=True)
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

    def _init_ui_elements(self):
        pass
