import vlc
#from Meta import vlc

class Player:

    def __init__(self, vlcInstance):
        self.vlcInstance = vlcInstance
        self.vlcPlayer = self.vlcInstance.media_player_new()
        self.volume = 50

    def SetFile(self, fileName, position):
        self.media = self.vlcInstance.media_new(fileName)
        self.vlcPlayer.set_media(self.media)
        self.vlcPlayer.play()
        self.vlcPlayer.set_position(position)
        self.vlcPlayer.pause()

    def PlayPause(self):
        if self.vlcPlayer.is_playing():
            self.vlcPlayer.pause()
        else:
            self.vlcPlayer.play()
    
    def GetPosition(self):
        return self.vlcPlayer.get_position()

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

