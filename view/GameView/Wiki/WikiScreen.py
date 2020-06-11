"""
Implements wiki screen displaying helpful information to the player
"""
import logging
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
    with open("assets/Wiki/Gadget.html") as f:
        _gadget_html = f.read()
        _gadget_html = _gadget_html.replace("\n", "")

    with open("assets/Wiki/Property.html") as f:
        _property_html = f.read()
        _property_html = _property_html.replace("\n", "")

    with open("assets/Wiki/character.html") as f:
        _character_html = f.read()
        _character_html = _character_html.replace("\n", "")

    with open("assets/Wiki/scenario.html") as f:
        _scenario_html = f.read()
        _scenario_html = _scenario_html.replace("\n", "")

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
                self.scenario_button: self._scenario_pressed
            }

            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Could not find UI-Element in dict")

    def _gadget_pressed(self) -> None:
        self.info_tb.html_text = self._gadget_html
        self.info_tb.rebuild()

    def _properties_pressed(self) -> None:
        self.info_tb.html_text = self._property_html
        self.info_tb.rebuild()

    def _character_pressed(self) -> None:
        self.info_tb.html_text = self._character_html
        self.info_tb.rebuild()

    def _scenario_pressed(self) -> None:
        self.info_tb.html_text = self._scenario_html
        self.info_tb.rebuild()

    def _init_ui_elements(self) -> None:
        self.info_tb = pygame_gui.elements.UITextBox(
            html_text="Select any of the buttons on the left to display helpful information",
            relative_rect=pygame.Rect((0, 0),
                                      (self.tb_container.rect.width, self.tb_container.rect.height)),
            manager=self.manager,
            container=self.tb_container,
            object_id="#info_textbox"
        )

        self.gadget_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Gadgets",
            manager=self.manager,
            container=self.selection_container
        )

        self.property_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.selection_container.elements)), self.__buttonSize),
            text="Properties",
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
