import logging
from typing import Dict
import pygame_gui.elements.ui_button
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu


class SettingsScreen(BasicView):
    _valid_resolutions = ["1024x576", "1152x648", "1366x768", "1600x900", "1920x1080", "2560x1440", "3840x2160"]

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, parentView, settings: ViewSettings):
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
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)
        self.__sliderSize = (self.container.rect.width / 3, self.container.rect.width / 15)

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
        logging.info("Button pressed")

    def return_button_pressed(self) -> Dict:
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
        :return:    None
        """
        self.address_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__buttonSize),
            html_text="<strong>Server Address</strong>",
            manager=self.manager,
            container=self.containerLabels
        )

        self.port_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__buttonSize),
            html_text="<strong>Port</strong>",
            manager=self.manager,
            container=self.containerLabels
        )

        self.resolution_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__buttonSize),
            html_text="<strong>Resolution</strong>",
            manager=self.manager,
            container=self.containerLabels
        )

        self.audio_music_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__buttonSize),
            html_text="<strong>Music</strong>",
            manager=self.manager,
            container=self.containerLabels
        )

        self.audio_effects_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.containerLabels.rect.centerx,
                                       self.containerLabels.rect.centery + self.__padding * len(
                                           self.containerLabels.elements)),
                                      self.__buttonSize),
            html_text="<strong>Effects</strong>",
            manager=self.manager,
            container=self.containerLabels
        )

        self.address_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container,
        )
        self.port_textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container,
        )

        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self._valid_resolutions,
            starting_option="Select Resolution",
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(
                                           self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container
        )

        self.audio_effects_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * (len(
                                           self.container.elements) - 1)),
                                      self.__sliderSize),
            start_value=50,
            value_range=(0, 100),
            manager=self.manager,
            container=self.container
        )

        self.audio_music_slider_ = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * (len(
                                           self.container.elements) - 2)),
                                      self.__sliderSize),
            start_value=50,
            value_range=(0, 100),
            manager=self.manager,
            container=self.container
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
