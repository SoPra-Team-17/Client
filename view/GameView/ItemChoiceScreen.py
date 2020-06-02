"""
Implements the screen in which the item choice is visualized
"""
import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.Visuals.VisualGadget import GADGET_NAME_LIST, GADGET_PATH_LIST
from view.GameView.Visuals.VisualCharacter import CHAR_PATH_LIST
from controller.ControllerView import ControllerGameView
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "08.05.2020 (doc creation)"


class ItemChoiceScreen(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView, parentView,
                 settings: ViewSettings) -> None:
        super(ItemChoiceScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView
        self.__img_size = (128, 128)

        self.manager = self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                                           "assets/GameView/GameViewTheme.json")

        self.bottom_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .465, self.settings.window_height * .75),
                                      (self.settings.window_width / 4, self.settings.window_height / 8)),
            manager=self.manager)

        self.char_img_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width / 2 - self.__img_size[0] * 2.5,
                                       self.settings.window_height / 2 - self.__img_size[1] * 2),
                                      (self.__img_size[0] * 5, self.__img_size[1])),
            manager=self.manager
        )

        self.char_name_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width / 2 - self.__img_size[0] * 2.5,
                                       self.settings.window_height / 2 - self.__img_size[1]),
                                      (self.__img_size[0] * 5, self.__img_size[1] / 2)),
            manager=self.manager
        )

        self.gadget_img_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width / 2 - self.__img_size[0] * 2.5,
                                       self.settings.window_height / 2 + self.__img_size[1] / 2),
                                      (self.__img_size[0] * 5, self.__img_size[1])),
            manager=self.manager
        )

        self.gadget_name_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width / 2 - self.__img_size[0] * 2.5,
                                       self.settings.window_height / 2 + self.__img_size[1] * 1.5),
                                      (self.__img_size[0] * 5, self.__img_size[1] / 2)),
            manager=self.manager
        )

        self.waiting_label_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width / 2 - self.__img_size[0] * 2.5,
                                       self.settings.window_height / 2 - self.__img_size[1] / 2),
                                      (self.__img_size[0] * 5, self.__img_size[1])),
            manager=self.manager
        )

        self.__padding = self.bottom_container.rect.width / 10
        self.__button_size = (self.bottom_container.rect.width / 3, self.bottom_container.rect.width / 12)
        self.__img_pad = 2 * self.__img_size[0]

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        # font with which the descriptions are rendered
        self.font = pygame.font.Font("assets/GameView/Montserrat-Regular.ttf", 20)

        self._init_ui_elements()

        logging.info("Itemchoice init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self._check_character_hover()

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            self.selected_item(event.ui_element)
            self._kill_ui_elements()

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "RequestItemChoice":
                logging.info("Update selection based on new Item Choices")
                self.update_selection()
            elif event.message_type == "RequestEquipmentChoice":
                logging.info("Entering equipment choice phase")
                self.parent_view.to_equipment()

        # todo debug, has to be removed at some point
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.controller.to_main_menu()

        if len(self.gadget_img_list) == 0 and len(self.char_img_list) == 0:
            self.waiting_label.set_text("Selection done. Waiting for other player.")

    def _check_character_hover(self) -> None:
        """
        Check if character image is currently hovered, if so init private textbox on this char
        :return:    None
        """
        if self.private_textbox is not None:
            self.private_textbox.kill()
            self.private_textbox = None

        for idx, button in enumerate(self.char_img_list):
            if button.check_hover(1 / self.settings.frame_rate, False):
                self._init_private_textbox(idx)

    def selected_item(self, element) -> None:
        """
        todo variable length --> index out of range can occur
        :param element:
        :return:
        """
        gadget = True
        try:
            index = self.gadget_img_list.index(element)
        except ValueError:
            gadget = False
            index = self.char_img_list.index(element)

        logging.info(f"Gadget: {gadget} Index: {index}")

        try:
            if gadget:
                self.controller.send_item_choice(
                    self.controller.lib_client_handler.lib_client.getOfferedGadgets()[index])
            else:
                self.controller.send_item_choice(
                    self.controller.lib_client_handler.lib_client.getOfferedCharacters()[index])
        except IndexError:
            logging.error("Index out of range at item choice")

    def update_selection(self) -> None:
        """
        call this method, when a ItemChoiceMessage is received!
        :return:    None
        """
        offeredCharacters = self.controller.lib_client_handler.lib_client.getOfferedCharacters()
        offeredGadgets = self.controller.lib_client_handler.lib_client.getOfferedGadgets()

        self._create_selection_buttons(len(offeredGadgets), len(offeredCharacters))

        for idx, gad in enumerate(offeredGadgets):
            img = pygame.image.load(GADGET_PATH_LIST[gad])
            img = pygame.transform.scale(img, self.__img_size)
            self.gadget_img_list[idx].normal_image = img
            self.gadget_img_list[idx].hovered_image = self.font.render(GADGET_NAME_LIST[gad], True, (255, 255, 255))
            self.gadget_img_list[idx].rebuild()

            self.gadget_name_list[idx].set_text(GADGET_NAME_LIST[gad])
            self.gadget_name_list[idx].rebuild()

        for idx, char_id in enumerate(offeredCharacters):
            # todo: img and text has to be set for characters!
            for char in self.controller.lib_client_handler.lib_client.getCharacterSettings():
                if char_id == char.getCharacterId():
                    # hier können jetzt eigenschaften aus characterdescription extrahiert werden
                    name = char.getName()
                    gender = char.getGender()
                    feature_list = char.getFeatures()

                    self.char_name_list[idx].set_text(name)
                    self.char_name_list[idx].rebuild()

                    self.char_gender_list.insert(idx, gender)

                    self.char_img_list[idx].normal_image = pygame.image.load(CHAR_PATH_LIST[0])
                    # todo pygame does not support rendering of escape characters!
                    self.char_img_list[idx].hovered_image = self.font.render(name, True,
                                                                             (255, 255, 255))
                    self.char_img_list[idx].rebuild()

    def _create_selection_buttons(self, gadget_len, char_len) -> None:

        for i in range(char_len):
            self.char_img_list.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.__img_pad * len(self.char_img_list), 0),
                                          self.__img_size),
                text="",
                manager=self.manager,
                container=self.char_img_container,
                object_id=f"#char_img0{i}"
            ))

            self.char_name_list.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (self.__img_pad * len(self.char_name_list), 0),
                    (self.__img_size[0], self.__img_size[1] / 2)),
                text=f"TestChar{i}",
                manager=self.manager,
                container=self.char_name_container,
                object_id=f"#name_label0{i}"
            ))

        for i in range(gadget_len):
            self.gadget_img_list.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.__img_pad * len(self.gadget_img_list), 0),
                                          self.__img_size),
                text="",
                manager=self.manager,
                container=self.gadget_img_container,
                object_id=f"#gadget_img0{i}"
            ))
            self.gadget_name_list.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    (self.__img_pad * len(self.gadget_name_list), 0),
                    (self.__img_size[0], self.__img_size[1] / 2)),
                text=f"",
                manager=self.manager,
                container=self.gadget_name_container,
                object_id=f"#name_label0{i}"
            ))

    def _init_ui_elements(self) -> None:
        self.gadget_img_list = []
        self.gadget_name_list = []
        self.char_img_list = []
        self.char_name_list = []
        self.char_gender_list = []
        self.char_feature_list = []
        self.private_textbox = None
        self.waiting_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.__img_size[0] * 5, self.__img_size[1])),
            text="",
            manager=self.manager,
            container=self.waiting_label_container,
            object_id="#waiting_label"
        )

    def _init_private_textbox(self, idx) -> None:

        # Creates a new textbox, which displays relevant information. Is placed above the hovered character image

        self.private_textbox = pygame_gui.elements.UITextBox(
            html_text=f"Gender: <b>{self.char_gender_list[idx]}</b> Features:",
            relative_rect=pygame.Rect((self.__img_pad * idx, 0),
                                      self.__img_size),
            manager=self.manager,
            container=self.char_img_container,
            object_id="#private_textbox"
        )

    def _kill_ui_elements(self) -> None:
        for img, name in zip(self.char_img_list, self.char_name_list):
            img.kill()
            name.kill()

        for img, name in zip(self.gadget_img_list, self.gadget_name_list):
            img.kill()
            name.kill()

        self.char_name_list.clear()
        self.char_img_list.clear()
        self.gadget_name_list.clear()
        self.gadget_img_list.clear()
        self.char_gender_list.clear()
        self.char_feature_list.clear()
