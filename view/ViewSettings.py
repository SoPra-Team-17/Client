import ipaddress

class ViewSettings:
    """
    Class implementing a state information of the current view settings
    The settings can be changed from the MainMenu or InGame
    """

    def __init__(self):
        self.window_width = 1920
        self.window_height = 1080
        self.window_name = "No Time to Spy"
        self.frame_rate = 60
        self.audio_effects = 50
        self.audio_music = 50
        self.address = ipaddress.ip_address("127.0.0.1")
        self.port = 1337

    def __repr__(self) -> str:
        """
        Returning string representation of settings
        :return:    string
        """
        return \
            f"WindowName: {self.window_name}\n"\
            f"Resolution: {self.window_width}x{self.window_height}\n"\
            f"Frame rate: {self.frame_rate}\n"\
            f"Audio effects: {self.audio_effects :.1f} Music: {self.audio_music :.1f}\n"\
            f"Server address: {self.address} Port: {self.port}\n"
