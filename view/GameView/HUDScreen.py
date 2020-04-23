import logging
import pygame_gui
import pygame


from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class HUDScreen(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings,
                 parent: BasicView):
        super(HUDScreen, self).__init__(window, controller, settings)

        self.parent = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/Menu/MainMenuTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .0, self.settings.window_height * 4 / 5),
                                      (self.settings.window_width, self.settings.window_height / 5)),
            manager=self.manager
        )

        self.__padding = self.container.rect.width / 10
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)

        self.background = pygame.Surface((self.container.rect.width, self.container.rect.height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, "dark_bg"))

        self.test_surface = pygame.image.load("assets/GameView/trash.png").convert_alpha()

        self._init_ui_elements()

        logging.info("HudScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, self.settings.window_height * 5 / 6))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.menu_button: self.menu_button_pressed
            }
            switcher.get(event.ui_element)()

    def menu_button_pressed(self):
        self.controller.to_main_menu()

    def _init_ui_elements(self) -> None:
        self.char_image_list = []
        self.health_bar_list = []

        for idx in range(6):
            self.char_image_list.append(
                pygame_gui.elements.UIImage(
                    relative_rect=pygame.Rect((idx * (128 + 15), 0), self.test_surface.get_size()),
                    image_surface=self.test_surface,
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image0{idx}"
                )
            )
            self.health_bar_list.append(
                pygame_gui.elements.UIScreenSpaceHealthBar(
                    relative_rect=pygame.Rect((idx * (128 + 15), 150), (128, 25)),
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#health_bar0{idx}"
                )
            )

        ip = 123
        mp = 456
        ap = 10
        chips = 12
        self.status_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<strong>Intelligence Points:</strong>{ip}<br><br><strong>Movement Points:</strong>{mp}<br><br>" \
                      f"<strong>Action Points:</strong>{ap}<br><br><strong>Chips:</strong>{chips}",
            relative_rect=pygame.Rect((len(self.char_image_list) * (128 + 15), 0), (300, 175)),
            manager=self.manager,
            container=self.container,
            object_id="#status_textbox"
        )

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((len(self.char_image_list) * (128 + 15) + 315, 100), (128, 25)),
            text="Menu",
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )
