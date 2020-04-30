import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class ItemChoiceScreen(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, parentView,
                 settings: ViewSettings) -> None:
        super(ItemChoiceScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.manager = self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                                           "assets/GameView/GameViewTheme.json")

        self.bottom_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .465, self.settings.window_height * .75),
                                      (self.settings.window_width / 4, self.settings.window_height / 8)),
            manager=self.manager)

        self.char_img_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .35, self.settings.window_height * .15),
                                      (self.settings.window_width * 3 / 2, self.settings.window_height / 4)),
            manager=self.manager
        )

        self.gadget_img_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .35, self.settings.window_height * .45),
                                      (self.settings.window_width * 3 / 2, self.settings.window_height / 4)),
            manager=self.manager
        )

        self.__padding = self.bottom_container.rect.width / 10
        self.__button_size = (self.bottom_container.rect.width / 3, self.bottom_container.rect.width / 12)
        self.__img_size = (128, 128)
        self.__img_pad = 2 * self.__img_size[0]

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
                self.start_game_button: self.start_game_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Did not find UI-Element in Dict")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.controller.to_main_menu()

    def start_game_pressed(self) -> None:
        self.parent_view.to_playing_field()

    def _init_ui_elements(self) -> None:
        self.test_char = pygame.image.load("assets/GameView/trash.png").convert_alpha()
        self.test_gadget = pygame.image.load("assets/GameView/axe.png").convert_alpha()

        self.char_img_list = []
        self.gadget_img_list = []

        for i in range(3):
            self.char_img_list.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((self.__img_pad * len(self.char_img_container.elements), 0),
                                              self.__img_size),
                    text="",
                    manager=self.manager,
                    container=self.char_img_container,
                    object_id=f"#char_img0{i}"
                )
            )

            self.gadget_img_list.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((self.__img_pad * len(self.gadget_img_container.elements), 0),
                                              self.__img_size),
                    text="",
                    manager=self.manager,
                    container=self.gadget_img_container,
                    object_id=f"#gadget_img0{i}"
                )
            )

        for char, gadget in zip(self.char_img_list, self.gadget_img_list):
            char.normal_image = self.test_char
            gadget.normal_image = self.test_gadget
            char.rebuild()
            gadget.rebuild()

        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.bottom_container.elements)), self.__button_size),
            text="Continue",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#start_game"
        )

