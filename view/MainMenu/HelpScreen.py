import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerMainMenu


class HelpScreen(BasicView):
    with open("assets/Menu/help_text.html") as f:
        _help_text = f.read()

    def __init__(self, window: pygame.display, controller: ControllerMainMenu, parentView,
                 settings: ViewSettings) -> None:
        super(HelpScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/Menu/MainMenuTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .1, self.settings.window_height * .2),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager
        )

        self.__padding = self.container.rect.width / 15
        self.__labelSize = (self.container.rect.width / 1.5, self.container.rect.width / 1.8)

        self.background = pygame.Surface((self.settings.window_width / 4, self.settings.window_height / 2))
        self.background.fill((20, 48, 11))

        self._init_ui_elements()

        logging.info("Help Screen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        """
        Receive event method, called by parent view. In this case Main Menu
        :param event:   event
        :return:        None
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent_view.to_main_menu()

    def _init_ui_elements(self) -> None:
        """
        In this method all the ui-elements are initialized

        :return:    None
        """

        self.help_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0,
                                       self.__padding * len(
                                           self.container.elements)),
                                      self.__labelSize),
            html_text=self._help_text,
            manager=self.manager,
            container=self.container,
            object_id="#help_textbox"
        )
