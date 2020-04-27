"""
Implements a event, caused by a new network message
"""
import pygame

__author__ = "Marco Deuscher"
__date__ = "27.04.2020 (creation)"

NETWORK_EVENT = "NETWORK"
NETWORK_EVENT_MESSAGE_TYPES = ["HelloReply", "GameStarted", "RequestItemChoice", "RequestEquipmentChoice", "GameStatus",
                               "RequestGameOperation", "Statistics", "GameLeft", "GamePause", "MetaInformation",
                               "Strike", "Error", "Replay"]

def create_network_event(vals: dict) -> None:
    """
    creates a network event, dict contains user_type to differentiate from pygame_gui events

    vals["message_type"] specifies the message type, possible types are
    {HelloReply, GameStarted, RequestItemChoice, RequestEquipmentChoice, GameStatus, RequestGameOperation,
    Statistics, GameLeft, GamePause, MetaInformation, Strike, Error, Replay}

    :param vals:    dict containing event information
    :return:        None
    """
    vals["user_type"] = "NETWORK"
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, vals))
