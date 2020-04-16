import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerLobby


class LobbyScreen(BasicView):
    _vald_roles = ["Player", "Spectator"]
    _text_labels = {
        "start_game": "Start Game",
        "reconnect": "Reconnect",
        "name": "Enter name",
        "role": "Select Role",
        "return": "Return"
    }

    def __init__(self, window: pygame.display, controller: ControllerLobby, parentView, settings: ViewSettings) -> None:
        super(LobbyScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/Menu/MainMenuTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .17, self.settings.window_height * .1),
                                      (self.settings.window_width / 4, self.settings.window_height / 2)),
            manager=self.manager)

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self._init_ui_elements()

        logging.info("Lobbyscreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.start_game_button.object_ids[0]: self.controller.to_game_view,
                self.reconnect_button.object_ids[0]: self.controller.send_reconnect,
                self.return_button.object_ids[0]: self.controller.to_main_menu
            }
            try:
                switcher.get(event.ui_object_id)()
            except TypeError:
                logging.warning("Did not find UI-Element in Dict")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.controller.to_main_menu()

    def _extract_info(self) -> dict:
        d = {}
        d["name"] = self.name_entryline.get_text()
        d["role"] = self.role_dropdown.selected_option

        return d

    def _init_ui_elements(self) -> None:
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text=self._text_labels["start_game"],
            manager=self.manager,
            container=self.container,
            object_id="#start_game"
        )

        self.reconnect_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text=self._text_labels["reconnect"],
            manager=self.manager,
            container=self.container,
            object_id="#reconnect"
        )

        self.name_entryline = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            manager=self.manager,
            container=self.container
        )

        self.role_dropdown = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            options_list=self._vald_roles,
            starting_option=self._text_labels["role"],
            manager=self.manager,
            container=self.container,
            object_id="#role_dropdown"
        )

        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.centerx,
                                       self.container.rect.centery + self.__padding * len(self.container.elements)),
                                      self.__buttonSize),
            text=self._text_labels["return"],
            manager=self.manager,
            container=self.container,
            object_id="#return"
        )

        self.name_entryline.set_text(self._text_labels["name"])
