"""
Implements interface between Specator view and controller
"""
import pygame

from view.BasicView import BasicView
from view.GameView.PlayingFieldScreen import PlayingFieldScreen
from view.GameView.SpectatorChoiceScreen import SpectatorChoiceScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerSpectatorView
from util.Coordinates import WorldPoint

__author__ = "Marco Deuscher"
__date__ = "04.06.20 (creation)"


class SpectatorView(BasicView):
    """
    This class implements the interface of the specator view class to the controller
    """

    def __init__(self, window: pygame.display, controller: ControllerSpectatorView, settings: ViewSettings):
        super(SpectatorView, self).__init__(window, controller, settings)

        self.playing_field_screen = PlayingFieldScreen(self.window, self.controller, self, self.settings)
        self.spectator_choice_screen = SpectatorChoiceScreen(self.window, self.controller, self, self.settings)

        self.active_views = [self.spectator_choice_screen]

    def draw(self) -> None:
        for view in self.active_views:
            view.draw()

        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        # todo filter events to hud!

        for view in self.active_views:
            view.receive_event(event)

    def to_playing_field(self) -> None:
        """
        This method implements the transition to the playing field, sets playing field and hud as active view
        Also updates playing field with the prev. received network update, same for hud screen
        :return: None
        """
        # todo add hud to active view
        self.active_views = [self.playing_field_screen]
        self.playing_field_screen.update_playingfield()
        # todo update hud

    def to_item_choice(self) -> None:
        """
        This method implements the transition to the item choice for the specator
        :return: None
        """
        self.active_views = [self.spectator_choice_screen]

    def get_selected_field(self) -> WorldPoint:
        """
        Getter for the currently selected playing field
        :return: WorldPoint or None if no field is selected
        """
        return self.playing_field_screen.map.get_selected_coords()
