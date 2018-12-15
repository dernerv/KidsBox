import pygame
import os
import eyed3

class MusicMetaData:
     def __init__(self, track, title, artist, album):
        self.track = track
        self.title = title
        self.artist = artist
        self.album = album

class MusicRepo:
    def __init__(self, rootFolder):
        self.rootFolder = rootFolder

    def GetSubFolders(self):
        return [name for name in os.listdir(self.rootFolder)
            if os.path.isdir(os.path.join(self.rootFolder, name))]

    def GetCover(self, foldername):
        subfolder = os.path.join(self.rootFolder, foldername)
        for name in os.listdir(subfolder):
            fileName = os.path.join(subfolder, name)
            if os.path.isfile(fileName):
                if (name.endswith(".png")):
                    return pygame.image.load(fileName)
    
    def GetInfo(self, filename):
        audiofile = eyed3.load(filename)
        return MusicMetaData(audiofile.tag.track_num, audiofile.tag.title, audiofile.tag.artist, audiofile.tag.album)

