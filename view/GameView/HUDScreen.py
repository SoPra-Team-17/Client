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

    __status_textbox_width = 200
    __info_textbox_width = 200
    # distance to set fix distance between character buttons
    __distance = 10
    # size of gadget and property icons
    __icon_size = 32
    __button_size = (150, 35)
    __dropdown_size = (200, 35)
    # todo: hack find better solution
    __hovering_threshold = 15

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings,
                 parent: BasicView) -> None:
        super(HUDScreen, self).__init__(window, controller, settings)

        self.parent = parent

        self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                            "assets/GUI/HUDTheme.json")

        self.container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .0, self.settings.window_height * 3 / 4),
                                      (self.settings.window_width, self.settings.window_height / 4)),
            manager=self.manager
        )

        # padding to set responsive size of character buttons
        self.__padding = (self.container.rect.width / 2 - 5 * self.__distance) / 7
        self.font = pygame.font.Font("assets/GameView/Montserrat-Regular.ttf", 20)

        self.background = pygame.Surface((self.container.rect.width, self.container.rect.height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, "dark_bg"))

        self._init_ui_elements()
        # initialising private_textbox to create the attribute in HUDScreen
        self._init_private_textbox(0)
        # kill private_textbox so that it does not appear on the screen
        self.private_textbox.kill()
        # set private_textbox to None as default value for receive_event method
        self.private_textbox = None

        self.__hovered_icon_idx = -1
        self.__hovered_count = 0


        logging.info("HudScreen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self._check_character_hover()
        self._update_textbox()

        self.window.blit(self.background, (0, self.container.rect.y))
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

    def menu_button_pressed(self) -> None:
        self.controller.to_main_menu()

    def send_action_pressed(self) -> None:
        logging.info(f"Selected Action: {self.action_bar.selected_option}")

    def _check_character_hover(self) -> None:
        # testing if character button idx is hovered, to show private_textbox
        # TODO: fix bug: "strange behavior on character button no. 1"
        for button in self.char_image_list:
            # if the mouse is hovering over a character button and there is no private_textbox
            if button.check_hover(1 / self.settings.frame_rate, False) and self.private_textbox is None:
                self._init_private_textbox(self.char_image_list.index(button))
                break
            elif not (button.check_hover(1 / self.settings.frame_rate, False)) and self.private_textbox:
                self.private_textbox.kill()
                self.private_textbox = None

    def _update_textbox(self) -> None:
        # todo: update info textbox text in here
        # check if any button is hovered --> update
        for idx, icon in enumerate(self.gadget_icon_list + self.property_icon_list):
            if icon.check_hover(1 / self.settings.frame_rate, False):
                if idx == self.__hovered_icon_idx:
                    self.__hovered_count += 1
                else:
                    self.__hovered_icon_idx = idx
                    continue

                if self.__hovered_count > self.__hovering_threshold:
                    self.info_textbox.html_text = f"Last hovered icon {idx}"
                    self.info_textbox.rebuild()
                    self.__hovered_count = 0
                break

    def _update_icons(self, char_len) -> None:
        gadget_icon_surface = pygame.image.load("assets/GameView/axe.png")
        gadget_icon_surface = pygame.transform.scale(gadget_icon_surface, [self.__icon_size] * 2)

        property_icon_surface = pygame.image.load("assets/GameView/ClammyClothes.png")
        property_icon_surface = pygame.transform.scale(property_icon_surface, [self.__icon_size] * 2)

        for idx_char in range(char_len):
            for idx in range(3):
                self.gadget_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + idx * self.__icon_size, 0),
                        gadget_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

        for idx_char in range(char_len):
            for idx in range(2):
                self.property_icon_list.append(pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        (idx_char * (self.__padding + self.__distance) + idx * self.__icon_size, self.__icon_size),
                        gadget_icon_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#gadget_image0{idx_char}"
                ))

        for gad in self.gadget_icon_list:
            gad.normal_image = gadget_icon_surface
            gad.rebuild()

        for prop in self.property_icon_list:
            prop.normal_image = property_icon_surface
            prop.rebuild()

    def _create_character_images(self, char_len) -> None:
        # test_surface to display images on character buttons
        char_surface = pygame.image.load("assets/GameView/trash.png").convert_alpha()
        char_surface = pygame.transform.scale(char_surface, (int(self.__padding), int(self.__padding)))

        for idx in range(char_len):
            self.char_image_list.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 2 * self.__icon_size),
                                              char_surface.get_size()),
                    text="",
                    manager=self.manager,
                    container=self.container,
                    object_id=f"#char_image0{idx}"
                )
            )
            self.health_bar_list.append(
                pygame_gui.elements.UIScreenSpaceHealthBar(
                    relative_rect=pygame.Rect(
                        (idx * (self.__padding + self.__distance),
                         self.__padding + self.__distance + 2 * self.__icon_size),
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
            relative_rect=pygame.Rect(
                (len(self.char_image_list) * (self.__padding + self.__distance), 0),
                (self.__status_textbox_width, self.container.get_rect().height)),
            manager=self.manager,
            container=self.container,
            object_id="#status_textbox"
        )

        # loading sample image on character buttons
        for char in self.char_image_list:
            char.normal_image = char_surface
            char.rebuild()

    def _init_ui_elements(self) -> None:
        self.char_image_list = []
        self.health_bar_list = []
        self.status_textbox = None

        self._create_character_images(3)

        self.gadget_icon_list = []
        self.property_icon_list = []
        self._update_icons(3)

        # implementing a dropdown action_bar with all actions a character can perform
        self.action_bar = pygame_gui.elements.UIDropDownMenu(
            options_list=self.__actionbar_options,
            starting_option=self.__actionbar_starting_opt,
            relative_rect=pygame.Rect(
                (self.container.rect.width - 2 * self.__distance - self.__button_size[0] - self.__status_textbox_width -
                 self.__dropdown_size[0], self.container.rect.height - self.__dropdown_size[1]),
                self.__dropdown_size),
            manager=self.manager,
            container=self.container,
            object_id="#action_bar",
        )

        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__button_size[0], self.container.rect.height - self.__button_size[1]),
                (self.__button_size)),
            text="Menu",
            manager=self.manager,
            container=self.container,
            object_id="#menu_button"
        )

        self.send_action_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.container.rect.width - self.__button_size[0],
                                       self.container.rect.height - 2 * self.__button_size[1] - self.__distance),
                                       (self.__button_size)),
                                      text="Send Action",
                                      manager=self.manager,
                                      container=self.container,
                                      object_id="#send_action"

                                      )

        self.info_textbox = pygame_gui.elements.UITextBox(
            html_text="Test123",
            relative_rect=pygame.Rect(
                (self.container.rect.width - self.__button_size[0] - self.__distance - self.__info_textbox_width, 0),
                (self.__info_textbox_width, self.container.rect.height)),
            manager=self.manager,
            container=self.container,
            object_id="info_textbox"
        )

        # private_textbox to show private character information by hovering

    def _init_private_textbox(self, idx) -> None:
        self.private_textbox = pygame_gui.elements.UITextBox(
            html_text=f"<b>HP:</b>{42}<br><b>IP:</b>{13}<br><b>Chips:</b>{13}<br>",
            relative_rect=pygame.Rect((idx * (self.__padding + self.__distance), 2 * self.__icon_size),
                                      (self.__padding, self.__padding)),
            manager=self.manager,
            container=self.container,
            object_id="#private_textbox"
        )
