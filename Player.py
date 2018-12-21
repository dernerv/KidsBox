import vlc
from vlc import EventType

class Player:

    def __init__(self, vlcInstance):
        self.vlcInstance = vlcInstance
        self.vlcPlayer = self.vlcInstance.media_player_new()
        self.event_manager = self.vlcPlayer.event_manager()
        self.volume = 50

    def set_event_end_callback(self, callback):
        self.event_manager.event_attach(EventType.MediaPlayerEndReached, callback)

    def set_event_position_changed_callback(self, callback):
        self.event_manager.event_attach(EventType.MediaPlayerPositionChanged, callback)

    def SetFile(self, fileName, position):
        self.vlcPlayer.stop()
        self.media = self.vlcInstance.media_new(fileName)
        self.vlcPlayer.set_media(self.media)
        self.vlcPlayer.play()
        self.vlcPlayer.set_position(position)

    def PlayPause(self):
        if self.vlcPlayer.is_playing():
            self.vlcPlayer.pause()
        else:
            self.vlcPlayer.play()
    
    def GetPosition(self):
        return self.vlcPlayer.get_position()

    def IsPlaying(self):
        return self.vlcPlayer.is_playing()

    def Stop(self):
        return self.vlcPlayer.stop()

    def Volume(self, volume):
        self.volume = volume
        self.vlcPlayer.audio_set_volume(self.volume)

    def VolumeUp(self):
        if self.volume < 100:
            self.volume += 1
        self.vlcPlayer.audio_set_volume(self.volume)
    
    def VolumeDown(self):
        if self.volume > 0:
            self.volume -= 1
        self.vlcPlayer.audio_set_volume(self.volume)

