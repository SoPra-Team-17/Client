"""
Implements the actual settings screen
"""

import logging
import validators
import pygame_gui.elements.ui_button
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class SettingsScreen(BasicView):
    _valid_resolutions = ["1024x576", "1152x648", "1366x768", "1600x900", "1920x1080", "2560x1440", "3840x2160"]
    _valid_port_inputs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    _text_labels = {
        "address_text": "Server Address",
        "port_text": "Port",
        "resolution_text": "Resolution",
        "music_text": "Music",
        "effects_text": "Effects"
    }
    _start_value_slider = {
        "effects_start": 50.0,
        "music_start": 50.0
    }
    _range_slider = {
        "effects_range": (0.0, 100.0),
        "music_range": (0.0, 100.0)
    }

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, parentView,
                 settings: ViewSettings) -> None:
        super(SettingsScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .45, self.settings.window_height * .4),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager
        )
        self.containerLabels = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .25, self.settings.window_height * .4),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager
        )

        self.__padding = self.container.rect.width / 15
        self.__buttonSize = (self.container.rect.width / 2, self.container.rect.width / 12)
        self.__labelSize = (self.container.rect.width / 3, self.container.rect.width / 15)
        self.__sliderSize = (self.container.rect.width / 2, self.container.rect.width / 15)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        logging.info("Settings Screen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        """
        Receive event method, called by parent view. In this case MainMenu
        :param event:   event
        :return:        None
        """
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.return_button: self.return_button_pressed,
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Did not find UI-Element in Dict")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.return_button_pressed()

    def return_button_pressed(self) -> None:
        """
        Callback when return button is pressed
        :return:    Dict containing the entered settings
        """
        try:
            width, height = self.resolution_dropdown.selected_option.split("x")
            width, height = int(width), int(height)
            # todo changing the resolution does not work atm! has to be implemented see issue
            # self.settings.window_height, self.settings.window_width = height, width
        except ValueError:
            logging.warning("Unable to parse Resolution")

        address_entry = self.address_entryline.get_text()
        valid_ipv4 = validators.ipv4(address_entry)
        valid_ipv6 = validators.ipv6(address_entry)
        valid_domain = validators.domain(address_entry)

        if valid_ipv4 or valid_ipv6 or valid_domain:
            self.settings.address = address_entry

        try:
            self.settings.port = int(self.port_entryline.get_text())
        except ValueError:
            logging.warning("Unable to parse port")

        self.settings.audio_effects = self.audio_effects_slider.get_current_value()
        self.settings.audio_music = self.audio_music_slider.get_current_value()

        self.settings.to_json()
        logging.info(self.settings)

        self.parent_view.to_main_menu()

    def _init_ui_elements(self) -> None:
        """
        In this method all the ui-elements are initialized
        todo slider need double the padding, is at the moment hardcoded
        :return:    None
        """
        self.address_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__labelSize),
            text=self._text_labels["address_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#address_label"
        )

        self.port_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.__padding * len(self.containerLabels.elements)), self.__labelSize),
            text=self._text_labels["port_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#port_label",
        )

        self.resolution_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.__padding * len(self.containerLabels.elements)), self.__labelSize),
            text=self._text_labels["resolution_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#resolution_label"
        )

        self.audio_music_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.__padding * (len(self.containerLabels.elements) + 1)), self.__labelSize),
            text=self._text_labels["music_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#audio_music_label"
        )

        self.audio_effects_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.__padding * (len(self.containerLabels.elements) + 1)), self.__labelSize),
            text=self._text_labels["effects_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#audio_effects_label"
        )

        self.address_entryline = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            manager=self.manager,
            container=self.container,
            object_id="#address_textbox"
        )
        self.port_entryline = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            manager=self.manager,
            container=self.container,
            object_id="#port_textbox"
        )

        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self._valid_resolutions,
            starting_option=f"{self.settings.window_width}x{self.settings.window_height}",
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            manager=self.manager,
            container=self.container,
            object_id="#resolution_dropdown"
        )

        self.audio_effects_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, self.__padding * (len(self.container.elements) - 1)), self.__sliderSize),
            start_value=self._start_value_slider["effects_start"],
            value_range=self._range_slider["effects_range"],
            manager=self.manager,
            container=self.container,
            object_id="#audio_effects_slider"
        )

        self.audio_music_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, self.__padding * (len(self.container.elements) - 2)), self.__sliderSize),
            start_value=self._start_value_slider["music_start"],
            value_range=self._range_slider["music_range"],
            manager=self.manager,
            container=self.container,
            object_id="#audio_music_slider"
        )

        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.container.elements)), self.__buttonSize),
            text="Return",
            manager=self.manager,
            container=self.container,
            object_id="#return_button"
        )

        self.address_entryline.set_text(f"{self.settings.address}")

        self.port_entryline.set_text(f"{self.settings.port}")
        self.port_entryline.allowed_characters = self._valid_port_inputs[:-1]

        self.audio_effects_slider.set_current_value(self.settings.audio_effects)
        self.audio_music_slider.set_current_value(self.settings.audio_music)
