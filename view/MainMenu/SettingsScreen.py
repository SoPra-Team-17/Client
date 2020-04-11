import logging
import pygame_gui.elements.ui_button
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu


class SettingsScreen(BasicView):
    _valid_resolutions = ["1024x576", "1152x648", "1366x768", "1600x900", "1920x1080", "2560x1440", "3840x2160"]
    _text_labels = {
        "address_text": "Server Address",
        "port_text": "Port",
        "resolution_text": "Resolution",
        "resolution_select_text": "Select Resolution",
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

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height),
                                            "assets/Menu/MainMenuTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.window_width * .17, self.window_height * .0),
                                      (self.window_width / 4, self.window_height / 2)),
            manager=self.manager
        )
        self.containerLabels = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.window_width * .05, self.window_height * 0),
                                      (self.window_width / 4, self.window_height / 2)),
            manager=self.manager
        )

        self.__padding = self.container.rect.width / 15
        self.__buttonSize = (self.container.rect.width / 2, self.container.rect.width / 12)
        self.__labelSize = (self.container.rect.width / 3, self.container.rect.width / 15)
        self.__sliderSize = (self.container.rect.width / 2, self.container.rect.width / 15)

        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        logging.info("Settings Screen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        """
        Receive event method, called by parent view. In this case MainMenu
        :param event:   event
        :return:        None
        """
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.return_button.object_ids[0]: self.return_button_pressed,
            }
            try:
                switcher.get(event.ui_object_id)()
            except TypeError:
                logging.warning("Did not find UI-Element in Dict")

    def default_callback(self) -> None:
        """
        Default callback for debug purposes
        :return:
        """
        logging.info("Default callback")

    def return_button_pressed(self) -> None:
        """
        Callback when return button is pressed
        :return:    Dict containing the entered settings
        """
        settings = {}
        settings["audio_effects"] = self.audio_effects_slider.get_current_value()
        settings["audio_music"] = self.audio_music_slider_.get_current_value()
        settings["resolution"] = self.resolution_dropdown.selected_option
        settings["address"] = self.address_textbox.get_text()
        settings["port"] = self.port_textbox.get_text()

        self.parent_view.to_main_menu(settings)

    def _init_ui_elements(self) -> None:
        """
        In this method all the ui-elements are initialized
        todo slider need double the padding, is at the moment hardcoded
        :return:    None
        """
        self.address_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__labelSize),
            text=self._text_labels["address_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#address_label"
        )

        self.port_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__labelSize),
            text=self._text_labels["port_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#port_label",
        )

        self.resolution_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__labelSize),
            text=self._text_labels["resolution_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#resolution_label"
        )

        self.audio_music_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * (len(
                                           self.containerLabels.elements) + 1)),
                                      self.__labelSize),
            text=self._text_labels["music_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#audio_music_label"
        )

        self.audio_effects_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * (len(
                                           self.containerLabels.elements) + 3)),
                                      self.__labelSize),
            text=self._text_labels["effects_text"],
            manager=self.manager,
            container=self.containerLabels,
            object_id="#audio_effects_label"
        )

        self.address_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container,
            object_id="#address_textbox"
        )
        self.port_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container,
            object_id="#port_textbox"
        )

        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self._valid_resolutions,
            starting_option=self._text_labels["resolution_select_text"],
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container,
            object_id="#resolution_dropdown"
        )

        self.audio_effects_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * (len(
                                           self.container.elements) - 1)),
                                      self.__sliderSize),
            start_value=self._start_value_slider["effects_start"],
            value_range=self._range_slider["effects_range"],
            manager=self.manager,
            container=self.container,
            object_id="#audio_effects_slider"
        )

        self.audio_music_slider_ = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * (len(
                                           self.container.elements) - 2)),
                                      self.__sliderSize),
            start_value=self._start_value_slider["music_start"],
            value_range=self._range_slider["music_range"],
            manager=self.manager,
            container=self.container,
            object_id="#audio_music_slider"
        )

        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text="Return",
            manager=self.manager,
            container=self.container,
            object_id="#return_button"
        )
