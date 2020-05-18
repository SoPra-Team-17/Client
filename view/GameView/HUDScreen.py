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

        # distance to set fix distance between character buttons
        self.__distance = 10
        # padding to set responsive size of character buttons
        self.__padding = (self.container.rect.width / 2 - 5 * self.__distance) / 5
        self.__buttonSize = (self.container.rect.width / 3, self.container.rect.width / 12)
        self.font = pygame.font.Font("assets/GameView/Montserrat-Regular.ttf", 20)

        self.background = pygame.Surface((self.container.rect.width, self.container.rect.height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, "dark_bg"))

        # test_surface to display images on character buttons
        self.test_surface = pygame.image.load("assets/GameView/trash.png").convert_alpha()
        self.test_surface = pygame.transform.scale(self.test_surface, (int(self.__padding), int(self.__padding)))

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

        # TODO: loading personal character-information by hovering over a character button
        # testing if character button idx is hovered, to show private_textbox
        # currently the private_textbox is displayed, until you hover over a character button
        # then the private_textbox is killed
        for idx in range(5):
            if not(self.char_image_list[idx].check_hover(1, False)):
                self.private_textbox.full_redraw()
            else:
                self.private_textbox.kill()

    def menu_button_pressed(self):
        self.controller.to_main_menu()

    def _init_ui_elements(self) -> None:
        self.char_image_list = []
        self.health_bar_list = []

        for idx in range(5):
            self.char_image_list.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 0),
                                              self.test_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image0{idx}"
                )
            )
            self.health_bar_list.append(
                pygame_gui.elements.UIScreenSpaceHealthBar(
                    relative_rect=pygame.Rect(
                        (idx * (self.__padding + self.__distance), self.__padding + self.__distance),
                        (self.__padding, 25)),
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#health_bar0{idx}"
                )
            )

            # TODO: implementing dropdown action_bar_list with all actions a character can perform

        # loading sample image on character buttons
        for char in self.char_image_list:
            char.normal_image = self.test_surface
            char.rebuild()

        ip = 123
        mp = 456
        ap = 10
        chips = 12
        self.status_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<strong>Intelligence Points:</strong>{ip}<br><br><strong>Movement Points:</strong>{mp}<br><br>" \
                      f"<strong>Action Points:</strong>{ap}<br><br><strong>Chips:</strong>{chips}",
            relative_rect=pygame.Rect((len(self.char_image_list) * (self.__padding + self.__distance), 0), (200, 175)),
            manager=self.manager,
            container=self.container,
            object_id="#status_textbox"
        )

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.width - self.__padding, self.__padding + self.__distance),
                                      (self.__padding, 25)),
            text="Menu",
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )

        # test_textbox to show private character information
        self.private_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<strong>Blabla</strong>{123}<br><br><Blabla</strong>{456}<br><br>" \
                      f"<strong>Blabla</strong>{789}<br><br><strong>Blabla</strong>{101112}",
            relative_rect=pygame.Rect((len(self.char_image_list) * (self.__padding + self.__distance) + 210, 0), (200, 175)),
            manager=self.manager,
            container=self.container,
            object_id="#private_textbox"
        )