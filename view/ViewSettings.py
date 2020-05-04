"""
Class implementing the needed settings for each view, also provides serialization to and from json
"""
import ipaddress
import logging
import json

__author__ = "Marco Deuscher"
__date__ = "25.04.2020 (date of doc. creation)"


class ViewSettings:
    """
    Class implementing a state information of the current view settings
    The settings can be changed from the MainMenu or InGame
    """
    _settings_path = "assets/Menu/settings.json"

    def __init__(self):
        try:
            with open(self._settings_path, "r") as f:
                parsed_json = json.load(f)
                self.from_json(parsed_json)
        except json.JSONDecodeError:
            logging.error("Unable to parse from JSON")
            self.window_width = 1920
            self.window_height = 1080
            self.window_name = "No Time to Spy"
            self.frame_rate = 60
            self.audio_effects = 50
            self.audio_music = 50
            self.address = "127.0.0.1"
            self.port = 1337

        self.to_json()

    def __repr__(self) -> str:
        """
        Returning string representation of settings
        :return:    string
        """
        return \
            f"WindowName: {self.window_name}\n" \
            f"Resolution: {self.window_width}x{self.window_height}\n" \
            f"Frame rate: {self.frame_rate}\n" \
            f"Audio effects: {self.audio_effects :.1f} Music: {self.audio_music :.1f}\n" \
            f"Server address: {self.address} Port: {self.port}\n"

    def to_json(self) -> None:
        j = {}
        j["window_name"] = self.window_name
        j["resolution"] = f"{self.window_width}x{self.window_height}"
        j["frame_rate"] = self.frame_rate
        j["audio_effects"] = self.audio_effects
        j["audio_music"] = self.audio_music
        j["address"] = self.address
        j["port"] = self.port

        with open(self._settings_path, "w") as f:
            f.write(json.dumps(j))

    def from_json(self, j) -> None:
        self.window_name = j["window_name"]
        self.window_width, self.window_height = tuple(int(x) for x in j["resolution"].split("x"))
        self.frame_rate = j["frame_rate"]
        self.audio_effects = j["audio_effects"]
        self.audio_music = j["audio_music"]
        self.address = j["address"]
        self.port = j["port"]
