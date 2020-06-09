"""
Implements interface to Gameview between controller and view
"""
import pygame

from view.BasicView import BasicView
from view.GameView.PlayingFieldScreen import PlayingFieldScreen
from view.GameView.HUDView import HUDView
from view.GameView.ItemChoiceScreen import ItemChoiceScreen
from view.GameView.EquipmentScreen import EquipmentScreen
from view.GameView.SettingsView import SettingsView
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView
from util.Coordinates import WorldPoint

__author__ = "Marco Deuscher"
__date__ = "20.05.20 (doc creation)"


class GameView(BasicView):
    """
    This class implements the interface of the GameView classes to the main controller
    """

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings) -> None:
        super().__init__(window, controller, settings)

        self.playing_field_screen = PlayingFieldScreen(self.window, self.controller, self, self.settings)
        self.hud_view = HUDView(self.window, self.controller, self, self.settings)
        self.item_choice_screen = ItemChoiceScreen(self.window, self.controller, self, self.settings)
        self.equipment_screen = EquipmentScreen(self.window, self.controller, self, self.settings)
        self.settings_view = SettingsView(self.window, self.controller, self, self.settings)

        self.active_views = [self.item_choice_screen]

    def draw(self) -> None:
        self.window.fill((50, 50, 50))

        for view in self.active_views:
            view.draw()

        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        # make sure button clicks on the HUD are not handled in the playing field screen
        if event.type == pygame.MOUSEBUTTONUP and self.hud_view.filter_event(event):
            self.hud_view.receive_event(event)
            return

        for view in self.active_views:
            view.receive_event(event)

    def to_playing_field(self) -> None:
        """
        This method implements the transition to the playing field, sets playing_field_screen and hud_view as active
        Also updates the playing field, with the prev. received network update, same for hud screen
        :return:    None
        """
        self.active_views = [self.playing_field_screen, self.hud_view]
        self.playing_field_screen.update_playingfield()
        self.hud_view.hudScreen.network_update()

    def to_item_choice(self) -> None:
        """
        This method implements the transistion to the item choice phase and updates the selection of characters and items
        reiceved over the network
        :return:    None
        """
        self.active_views = [self.item_choice_screen]
        self.item_choice_screen.update_selection()

    def to_equipment(self) -> None:
        """
        This method implements the transisition to the equipment phase screen and updates the selection based on the prev.
        received network update
        :return:
        """
        self.active_views = [self.equipment_screen]
        self.equipment_screen.update_selection()

    def to_settings(self) -> None:
        """
        This method implements the transition to the setttings screen
        :return:    None
        """
        self.active_views = [self.settings_view]

    def get_selected_field(self) -> WorldPoint:
        """
        Getter for the currently selected playing field
        todo return type for invalid selection!
        :return:
        """
        return self.playing_field_screen.map.get_selected_coords()
