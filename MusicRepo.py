import pygame
import os
import json

class MusicRepo:
    def __init__(self, rootFolder, vlcInstance):
        self.vlcInstance = vlcInstance
        self.rootFolder = rootFolder
        self.albums = None

    def GetAlbums(self):
        if self.albums == None:
            self.albums = [name for name in os.listdir(self.rootFolder)
                            if os.path.isdir(os.path.join(self.rootFolder, name))]
        return self.albums

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
    
    def SavePosition(self, album_index, media_index, media_position):
        folder = self.albums[album_index]
        with open(self.rootFolder + "\\" + folder + "\\" + "position.json", "w") as write_file:
            data = {
                "fileIndex": media_index,
                "position": media_position
            }
            json.dump(data, write_file)

    def LoadPositionAndFile(self, album_index):
        try:
            with open(self.rootFolder + "\\" + self.folders[album_index] + "\\" + "position.json", "r") as read_file:
                return json.load(read_file)
        except:
            self.media_index = 0
            self.media_position = 0.0
            return {
                        "fileIndex": 0,
                        "position": 0
                    }    

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