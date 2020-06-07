"""
Implements interface between Specator view and controller
"""
import logging
import time
import pygame
import cppyy

from view.BasicView import BasicView
from view.GameView.PlayingFieldScreen import PlayingFieldScreen
from view.GameView.SpectatorChoiceScreen import SpectatorChoiceScreen
from view.GameView.SpectatorHUDScreen import SpectatorHUDScreen
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerSpectatorView
from util.Coordinates import WorldPoint
from network.NetworkEvent import NETWORK_EVENT

from cppyy.gbl.std import map, pair, set, vector

cppyy.add_include_path("/usr/local/include/SopraClient")
cppyy.add_include_path("/usr/local/include/SopraCommon")
cppyy.add_include_path("/usr/local/include/SopraNetwork")

cppyy.include("network/messages/MetaInformationKey.hpp")
cppyy.include("util/UUID.hpp")
cppyy.include("datatypes/character/FactionEnum.hpp")

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
        self.spectator_HUD_screen = SpectatorHUDScreen(self.window, self.controller, self, self.settings)

        self.active_views = [self.spectator_choice_screen]

        self.player_one_id = None
        self.player_two_id = None
        self.player_neutral_id = None

    def draw(self) -> None:
        for view in self.active_views:
            view.draw()

        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.USEREVENT and event.user_type == NETWORK_EVENT:
            if event.message_type == "MetaInformation":
                self._on_meta_received()
        for view in self.active_views:
            view.receive_event(event)

    def to_playing_field(self) -> None:
        """
        This method implements the transition to the playing field, sets playing field and hud as active view
        Also updates playing field with the prev. received network update, same for hud screen
        :return: None
        """
        # get metainformation, make sure message was alreafy received before updating
        key_list = [cppyy.gbl.spy.network.messages.MetaInformationKey.CONFIGURATION_CHARACTER_INFORMATION,
                    cppyy.gbl.spy.network.messages.MetaInformationKey.FACTION_PLAYER1,
                    cppyy.gbl.spy.network.messages.MetaInformationKey.FACTION_PLAYER2,
                    cppyy.gbl.spy.network.messages.MetaInformationKey.FACTION_NEUTRAL]
        ret = self.controller.send_request_meta_information(key_list)
        logging.info(f"Send Request Metainformation successfull: {ret}\nWaiting for Metainformation")

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

    def _on_meta_received(self):
        meta_info = self.controller.lib_client_handler.lib_client.getInformation()

        variant = meta_info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.FACTION_NEUTRAL]
        self.player_neutral_id = cppyy.gbl.std.get[vector[cppyy.gbl.spy.util.UUID]](variant)

        variant = meta_info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.FACTION_PLAYER1]
        self.player_one_id = cppyy.gbl.std.get[vector[cppyy.gbl.spy.util.UUID]](variant)

        variant = meta_info[
            cppyy.gbl.spy.network.messages.MetaInformationKey.FACTION_PLAYER2]
        self.player_two_id = cppyy.gbl.std.get[vector[cppyy.gbl.spy.util.UUID]](variant)

        # sort into libclient lists
        # todo uncomment when libclient is updated
        """
        for neutral_id in self.player_neutral_id:
            self.controller.lib_client_handler.lib_client.setFaction(neutral_id,
                                                                     cppyy.gbl.spy.character.FactionEnum.NEUTRAL)

        for player1_id in self.player_one_id:
            self.controller.lib_client_handler.lib_client.setFaction(player1_id,
                                                                     cppyy.gbl.spy.character.FactionEnum.PLAYER1)

        for player2_id in self.player_two_id:
            self.controller.lib_client_handler.lib_client.setFaction(player2_id,
                                                                     cppyy.gbl.spy.character.FactionEnum.PLAYER2)
        """

        # wait until meta information is received, then start game
        self.active_views = [self.playing_field_screen, self.spectator_HUD_screen]
        self.playing_field_screen.update_playingfield()
        self.spectator_HUD_screen.network_update()
