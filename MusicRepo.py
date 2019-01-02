import pygame
import os
import json

class MusicRepo:
    def __init__(self, rootFolder, vlcInstance):
        self.vlcInstance = vlcInstance
        self.rootFolder = rootFolder
        self.albums = None
        self.Covers = dict()
        self.files_in_album = dict()
        self.file_info = dict()


    def LoadAll(self):
        self.noCoverImage = pygame.image.load("no-cover.png")
        folders = self.GetAlbums()
        for folder in folders:
            files = self.GetFiles(folder)
            infos = []
            for filename in files:
                infos.append(self.GetInfo(filename))
            infos.sort(key=self.get_track_no)
            self.files_in_album[folder] = infos

    def get_track_no(self, element):
        if element.track == None:
            return 0
        return element.track

    def get_mediafiles(self, foldername):
        if len(self.files_in_album) < 1:
            return None
        return self.files_in_album[foldername]

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
        if foldername in self.Covers:
            return self.Covers[foldername]
        subfolder = os.path.join(self.rootFolder, foldername)
        for name in os.listdir(subfolder):
            fileName = os.path.join(subfolder, name)
            if os.path.isfile(fileName):
                if (name.endswith(".png")):
                    cover = pygame.image.load(fileName)
                    self.Covers[foldername] = cover
                    return cover
        return self.noCoverImage
    
    def SavePosition(self, album_index, media_index, media_position):
        folder = self.GetAlbums()[album_index]
        filename = self.rootFolder + "/" + folder + "/" + "position.json"
        #print("Save into file " + filename)
        with open(filename, "w") as write_file:
            data = {
                "fileIndex": media_index,
                "position": media_position
            }
            json.dump(data, write_file)

    def LoadPositionAndFile(self, album_index):
        try:
            folder = self.GetAlbums()[album_index]
            filename = self.rootFolder + "/" + folder + "/" + "position.json"
            print("Load file " + filename)
            with open(filename, "r") as read_file:
                return json.load(read_file)
        except:
            print("Loading failed")
            return {
                        "fileIndex": 0,
                        "position": 0
                    }    

    def GetInfo(self, filename):
        self.media = self.vlcInstance.media_new(filename)
        self.media.parse()
        return MusicMetaData(self.media.get_meta(5), self.media.get_meta(0), self.media.get_meta(1), self.media.get_meta(4), self.media.get_duration(), filename)


class MusicMetaData:
     def __init__(self, track, title, artist, album, duration, filename):
        self.track = track
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.filename = filename