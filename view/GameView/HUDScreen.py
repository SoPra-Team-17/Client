import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView


class HUDScreen(BasicView):
    # starting option of dropdown
    __actionbar_starting_opt = "Select Action"
    __actionbar_options = ["Gadget", "Gamble", "Spy", "Movement", "Retire", "Property"]

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings,
                 parent: BasicView):
        super(HUDScreen, self).__init__(window, controller, settings)

        self.parent = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/HUDTheme.json")

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
        # initialising private_textbox to create the attribute in HUDScreen
        self._init_private_textbox(0)
        # kill private_textbox so that it does not appear on the screen
        self.private_textbox.kill()
        # set private_textbox to None as default value for receive_event method
        self.private_textbox = None

    logging.info("HudScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self._check_character_hover()

        self.window.blit(self.background, (0, self.settings.window_height * 5 / 6))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            switcher = {
                self.menu_button: self.menu_button_pressed,
                self.send_action_button: self.send_action_pressed
            }
            try:
                switcher.get(event.ui_element)()
            except TypeError:
                logging.warning("Element not found in dict")

    def menu_button_pressed(self):
        self.controller.to_main_menu()

    def send_action_pressed(self):
        logging.info(f"Selected Action: {self.action_bar.selected_option}")


    def _check_character_hover(self):
        # testing if character button idx is hovered, to show private_textbox
        # TODO: fix bug: "strange behavior on character button no. 1"
        for button in self.char_image_list:
            # if the mouse is hovering over a character button and there is no private_textbox
            if button.check_hover(1, False) and self.private_textbox is None:
                self._init_private_textbox(self.char_image_list.index(button))
                break
            elif not (button.check_hover(1, False)) and self.private_textbox:
                self.private_textbox.kill()
                self.private_textbox = None

    def _create_character_images(self, char_len):
        for idx in range(char_len):
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

        # loading sample image on character buttons
        for char in self.char_image_list:
            char.normal_image = self.test_surface
            char.rebuild()

    def _init_ui_elements(self) -> None:
        self.char_image_list = []
        self.health_bar_list = []
        self.status_textbox = None

        self._create_character_images(3)

        # implementing a dropdown action_bar with all actions a character can perform
        self.action_bar = pygame_gui.elements.UIDropDownMenu(
            options_list=self.__actionbar_options,
            starting_option=self.__actionbar_starting_opt,
            relative_rect=pygame.Rect(
                (self.container.rect.width - 3 * self.__padding - self.__distance, self.__padding + self.__distance),
                (2 * self.__padding, 25)),
            manager=self.manager,
            container=self.container,
            object_id="#action_bar",
        )

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.width - self.__padding, self.__padding + self.__distance),
                                      (self.__padding, 25)),
            text="Menu",
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )

        self.send_action_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.width - self.__padding, self.__distance),
                                      (self.__padding, 25)),
            text="Send Action",
            manager=self.manager,
            container=self.container,
            object_id="#send_action"
        )

    # private_textbox to show private character information by hovering
    def _init_private_textbox(self, idx) -> None:

        self.private_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<b>Health Points:</b>{42}",
            relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 0),
                                      (self.__padding, 175)),
            manager=self.manager,
            container=self.container,
            object_id="#private_textbox"
        )
