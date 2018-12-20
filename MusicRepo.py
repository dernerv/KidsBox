import pygame
import os
#import eyed3

class MusicRepo:
    def __init__(self, rootFolder, vlcInstance):
        self.vlcInstance = vlcInstance
        self.rootFolder = rootFolder

    def GetSubFolders(self):
        return [name for name in os.listdir(self.rootFolder)
            if os.path.isdir(os.path.join(self.rootFolder, name))]

    def GetFiles(self, foldername):
        files = []
        subfolder = os.path.join(self.rootFolder, foldername)
        for name in os.listdir(subfolder):
            fileName = os.path.join(subfolder, name)
            if os.path.isfile(fileName):
                if (name.endswith(".mp3")):
                    files.append(fileName)
        return files

    def GetNumberOfFiles(self, foldername):    
        return len(self.GetFiles(foldername))

    def GetCover(self, foldername):
        subfolder = os.path.join(self.rootFolder, foldername)
        for name in os.listdir(subfolder):
            fileName = os.path.join(subfolder, name)
            if os.path.isfile(fileName):
                if (name.endswith(".png")):
                    return pygame.image.load(fileName)
    
    def GetInfo(self, filename):
        self.media = self.vlcInstance.media_new(filename)
        self.media.parse()
        return MusicMetaData(self.media.get_meta(5), self.media.get_meta(0), self.media.get_meta(1), self.media.get_meta(4))


class MusicMetaData:
     def __init__(self, track, title, artist, album):
        self.track = track
        self.title = title
        self.artist = artist
        self.album = album