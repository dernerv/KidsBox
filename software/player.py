import vlc
from vlc import EventType

class Player:

    def __init__(self, vlcInstance):
        self.vlcInstance = vlcInstance
        self.vlcPlayer = self.vlcInstance.media_player_new()
        
        self.event_manager = self.vlcPlayer.event_manager()
        self.current_volume = self.vlcPlayer.audio_get_volume()

    def set_event_end_callback(self, callback):
        self.event_manager.event_attach(EventType.MediaPlayerEndReached, callback)

    def set_event_position_changed_callback(self, callback):
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, callback)

    def set_file(self, fileName, position):
        self.vlcPlayer.stop()
        self.media = self.vlcInstance.media_new(fileName)
        self.vlcPlayer.set_media(self.media)
        self.vlcPlayer.play()
        self.vlcPlayer.set_position(position)

    def play_pause(self):
        if self.vlcPlayer.is_playing():
            self.vlcPlayer.pause()
        else:
            self.vlcPlayer.play()
    
    def get_position(self):
        return self.vlcPlayer.get_position()

    def is_playing(self):
        return self.vlcPlayer.is_playing()

    def stop(self):
        return self.vlcPlayer.stop()

    def set_volume(self, volume):
        self.current_volume = volume
        self.vlcPlayer.audio_set_volume(self.current_volume)

    def mute(self, volume):
        self.vlcPlayer.audio_set_volume(0)

    def unmute(self, volume):
        self.vlcPlayer.audio_set_volume(self.current_volume)

    def volume_up(self):
        if self.current_volume < 100:
            self.current_volume += 4
        self.vlcPlayer.audio_set_volume(self.current_volume)
    
    def volume_down(self):
        if self.current_volume > 0:
            self.current_volume -= 4
        self.vlcPlayer.audio_set_volume(self.current_volume)

