"""
Implements the screen in which the equipment phase is visualized
"""

import logging
import pygame_gui
import pygame

from view.BasicView import BasicView
from view.ViewSettings import ViewSettings
from view.GameView.Visuals.ItemChoice.VisualCharacter import CHAR_PATH_LIST
from view.GameView.Visuals.ItemChoice.VisualGadget import GADGET_NAME_LIST, GADGET_PATH_LIST
from controller.ControllerView import ControllerGameView
from network.NetworkEvent import NETWORK_EVENT

__author__ = "Marco Deuscher"
__date__ = "08.05.2020 (creation)"


class DrawableImage:

    def __init__(self, rect, surface, lib_client_obj=None):
        self.surface = surface
        self.rect = rect
        self.lib_client_obj = lib_client_obj

    def draw(self, window: pygame.display) -> None:
        window.blit(self.surface, self.rect)


class EquipmentScreen(BasicView):
    """
    Player prev. selected between 2 and 4 characters and 4 and 6 gadgets
    Now each gadgets has to be mapped to a character
    """

    def __init__(self, window: pygame.display, controller: ControllerGameView, parentView,
                 settings: ViewSettings) -> None:
        super(EquipmentScreen, self).__init__(window, controller, settings)

        self.parent_view = parentView

        self.__dragging = False
        self.__drag_index = 0

        # map from GadgetEnum -> UUID (char)
        self.gadget_char_map = {}
        # todo remove
        self.__debug = False

        self.manager = self.manager = pygame_gui.UIManager((self.settings.window_width, self.settings.window_height),
                                                           "assets/GameView/GameViewTheme.json")

        self.bottom_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((self.settings.window_width * .465, self.settings.window_height * .7),
                                      (self.settings.window_width / 4, self.settings.window_height / 8)),
            manager=self.manager)

        self.background = pygame.Surface((self.settings.window_width, self.settings.window_height))
        self.background.fill(self.manager.ui_theme.get_colour(None, None, 'dark_bg'))

        self.__padding = self.bottom_container.rect.width / 10
        self.__button_size = (self.bottom_container.rect.width / 3, self.bottom_container.rect.width / 12)
        self.__img_size = (128, 128)
        self.__img_pad = 2.25 * self.__img_size[0]

        self._init_ui_elements()

        logging.info("Equipment screen init done")

    def draw(self) -> None:
        self.manager.update(1 / self.settings.frame_rate)

        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)

        for char in self.characters:
            char.draw(self.window)

        for gad in self.gadgets:
            gad.draw(self.window)

    def receive_event(self, event: pygame.event.Event) -> None:
        self.manager.process_events(event)

        if len(self.gadgets) != 0:
            self._drag_and_drop(event)

        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "RequestItemChoice":
                logging.info("Go to Item Choice Phase")
                self.controller.to_game_view()

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            self.continue_pressed()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.controller.to_main_menu()

    def continue_pressed(self) -> None:
        if len(self.gadgets) != 0 and not self.__debug:
            logging.info("Not all gadgets owned by a character")
            return

        # convert map to uuid -> gadget
        network_map = {}
        for key, val in self.gadget_char_map.items():
            if val in network_map:
                network_map[val].append(key)
            else:
                network_map[val] = [key]

        self.controller.send_equipment_choice(network_map)
        self.parent_view.to_playing_field()

    def update_selection(self) -> None:
        selected_characters = self.controller.lib_client_handler.lib_client.getChosenCharacters()
        selected_gadgets = self.controller.lib_client_handler.lib_client.getChosenGadgets()

        print(selected_characters)
        print(selected_gadgets)

        for idx in range(selected_characters.size()):
            self.characters.append(DrawableImage(pygame.Rect(
                (self.settings.window_width * .1 + idx * self.__img_pad,
                 self.settings.window_height * .1),
                (128, 128)),
                # todo update assets
                pygame.image.load(CHAR_PATH_LIST[0]),
                selected_characters[idx]
            ))

        for idx in range(selected_gadgets.size()):
            self.gadgets.append(DrawableImage(pygame.Rect(
                (self.settings.window_width * .1 + idx * self.__img_pad, self.settings.window_height * .45),
                (128, 128)),
                pygame.image.load(GADGET_PATH_LIST[selected_gadgets[idx]]),
                selected_gadgets[idx]
            ))

        # anzahl der dragable elemente!
        self.__offset = [[0, 0]] * len(self.gadgets)

    def _drag_and_drop(self, event):
        # drag and drop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                for idx, gad in enumerate(self.gadgets):
                    if gad.rect.collidepoint(event.pos):
                        self.__dragging = True
                        self.__offset[idx][0] = self.gadgets[idx].rect.x - event.pos[0]
                        self.__offset[idx][1] = self.gadgets[idx].rect.y - event.pos[1]
                        self.__drag_index = idx
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.__dragging = False
                # check if dropped over target
                for char in self.characters:
                    if self.gadgets[self.__drag_index].rect.colliderect(char.rect):
                        self.gadget_char_map[self.gadgets[self.__drag_index].lib_client_obj] = char.lib_client_obj
                        self.gadgets.remove(self.gadgets[self.__drag_index])
                        break
        elif event.type == pygame.MOUSEMOTION:
            if self.__dragging:
                mouse_x, mouse_y = event.pos
                self.gadgets[self.__drag_index].rect.x = mouse_x + self.__offset[self.__drag_index][0]
                self.gadgets[self.__drag_index].rect.y = mouse_y + self.__offset[self.__drag_index][1]

        if len(self.gadgets) == 0:
            self.text_label.set_text("Equipment done")

    def _init_ui_elements(self) -> None:
        self.text_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, self.__padding * len(self.bottom_container.elements)), self.__button_size),
            text="",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#text_label"
        )

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, self.__padding * len(self.bottom_container.elements)), self.__button_size),
            text="Continue",
            manager=self.manager,
            container=self.bottom_container,
            object_id="#continue"
        )

        # this screen is only opened if the network message request requip mapping was already received
        self.gadgets = []
        self.characters = []

        if self.__debug:
            for idx in range(6):
                self.gadgets.append(DrawableImage(pygame.Rect(
                    (self.settings.window_width * .15 + idx * self.__img_pad, self.settings.window_height * .45),
                    (128, 128)
                ), pygame.image.load("assets/GameView/axe.png"), idx))

            for idx in range(2):
                self.characters.append(DrawableImage(pygame.Rect(
                    (self.settings.window_width * .15 + idx * self.__img_pad,
                     self.settings.window_height * .1),
                    (128, 128)),
                    pygame.image.load("assets/GameView/trash.png"), idx+10))

            # anzahl der dragable elemente!
            self.__offset = [[0, 0]] * len(self.gadgets)
