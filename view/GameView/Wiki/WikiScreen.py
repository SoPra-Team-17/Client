"""
Implements wiki screen displaying helpful information to the player
"""
import logging
import os

import pygame
import pygame_gui

from view.ViewSettings import ViewSettings
from view.BasicView import BasicView
from view.GameView.Visuals.VisualGadget import GADGET_NAME_LIST
from view.GameView.Visuals.VisualProperty import PROPERTY_NAME_LIST
from controller.ControllerView import ControllerGameView

__author__ = "Marco Deuscher"
__date__ = "10.06.2020"


class WikiScreen(BasicView):
    __path_list = [
        "assets/Wiki/Characters.html",
        "assets/Wiki/Draft.html",
        "assets/Wiki/Gadget.html",
        "assets/Wiki/Property.html",
        "assets/Wiki/Round.html",
        "assets/Wiki/Scenario.html",
        "assets/Wiki/Victory.html"
    ]
    __html_dict = {}
    for path in __path_list:
        with open(path) as f:
            key = os.path.basename(path).split('.')[0].lower()
            __html_dict[key] = f.read().replace("\n", "")

    def __init__(self, window: pygame.display, controller: ControllerGameView, parent, settings: ViewSettings) -> None:
        super(WikiScreen, self).__init__(window, controller, settings)

        self.parent_view = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/GUITheme.json")
        self.selection_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((0.05 * self.settings.window_width, 0.05 * self.settings.window_height),
                                      (0.25 * self.settings.window_width, 0.95 * self.settings.window_height)),
            manager=self.manager,
        )

        self.tb_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((0.3 * self.settings.window_width, 0.05 * self.settings.window_height),
                                      (0.65 * self.settings.window_width, 0.95 * self.settings.window_height)),
            manager=self.manager
        )

        self.__padding = self.settings.window_width / 30
        self.__buttonSize = (225, 40)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, "dark_bg"))

        self._init_ui_elements()

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.gadget_button: self._gadget_pressed,
                self.property_button: self._properties_pressed,
                self.character_button: self._character_pressed,
                self.scenario_button: self._scenario_pressed,
                self.victory_button: self._victory_pressed,
                self.round_button: self._round_pressed,
                self.draft_button: self._draft_pressed,
                self.return_button: self._return_pressed
            }

            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Could not find UI-Element in dict")

    def _gadget_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["gadget"]
        self.info_tb.rebuild()

    def _properties_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["property"]
        self.info_tb.rebuild()

    def _character_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["characters"]
        self.info_tb.rebuild()

    def _scenario_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["scenario"]
        self.info_tb.rebuild()

    def _draft_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["draft"]
        self.info_tb.rebuild()

    def _round_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["round"]
        self.info_tb.rebuild()

    def _victory_pressed(self) -> None:
        self.info_tb.html_text = self.__html_dict["victory"]
        self.info_tb.rebuild()

    def _return_pressed(self) -> None:
        self.parent_view.parent.to_settings()

    def _init_ui_elements(self) -> None:
        self.info_tb = pygame_gui.elements.UITextBox(
            html_text="Select any of the buttons on the left to display helpful information",
            relative_rect=pygame.Rect((0, 0),
                                      (self.tb_container.rect.width, self.tb_container.rect.height)),
            manager=self.manager,
            container=self.tb_container,
            object_id="#info_textbox"
        )

        self.draft_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Draft",
            manager=self.manager,
            container=self.selection_container
        )

        self.round_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Round",
            manager=self.manager,
            container=self.selection_container
        )

        self.scenario_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Scenario",
            manager=self.manager,
            container=self.selection_container
        )

        self.character_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Characters",
            manager=self.manager,
            container=self.selection_container
        )

        self.property_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Properties",
            manager=self.manager,
            container=self.selection_container
        )

        self.gadget_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Gadgets",
            manager=self.manager,
            container=self.selection_container
        )

        self.victory_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Victory",
            manager=self.manager,
            container=self.selection_container
        )

        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * (len(self.selection_container.elements) + 1)),
                                      self.__buttonSize),
            text="Return",
            manager=self.manager,
            container=self.selection_container
        )
