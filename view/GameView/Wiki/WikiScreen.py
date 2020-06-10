"""
Implements wiki screen displaying helpful information to the player
"""
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
            print(
                f"CurrentGadgetstate: {self.gadget_dropdown.current_state}\nCurrentPropState: {self.property_dropdown.current_state}")

    def _init_ui_elements(self) -> None:
        self.info_tb = pygame_gui.elements.UITextBox(
            html_text="Test html <b>Test</b>",
            relative_rect=pygame.Rect((0, 0),
                                      (self.tb_container.rect.width, self.tb_container.rect.height)),
            manager=self.manager,
            container=self.tb_container,
            object_id="#info_textbox"
        )

        self.gadget_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.selection_container.elements)),
                                      self.__buttonSize),
            text="Gadgets",
            manager=self.manager,
            container=self.selection_container
        )

        self.gadget_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=GADGET_NAME_LIST,
            starting_option="Select Gadget",
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.selection_container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.selection_container
        )

        self.property_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.selection_container.elements)),
                                      self.__buttonSize),
            text="Properties",
            manager=self.manager,
            container=self.selection_container
        )

        self.property_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=PROPERTY_NAME_LIST,
            starting_option="Select Property",
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.selection_container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.selection_container
        )
