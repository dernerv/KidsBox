import pygame
import sys, signal
import vlc
import json
import time

from Player import Player
from View import View
from MusicRepo import MusicRepo

class Controller:
    def __init__(self, display):
        self.display = display
        self.view = View(self.display)
        self.album_index = 0
        self.media_index = 0
        self.media_position = 0
        self.lastUpdate = 0.0
        self.albumMode = True
        self.rootFolder = "C:\\Users\\nerv\\sandbox"

    def setup(self):
        self.view.Welcome()
        self.vlcInstance = vlc.Instance()
        self.player = Player(self.vlcInstance)
        self.repo = MusicRepo(self.rootFolder, self.vlcInstance)
        self.folders = self.repo.GetSubFolders()
        self.noCoverImage = pygame.image.load("no-cover.png")

    def loop(self):
        clock = pygame.time.Clock()
        self.ShowAlbums()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q :
                        pygame.quit()
                        sys.exit(0)
                    if event.key == pygame.K_ESCAPE :
                        print("back")
                        self.albumMode = True
                        self.ShowAlbums()
                    if event.key == pygame.K_p :
                        print("enter / play-pause")
                        if self.albumMode:
                            fileAndPosition = self.LoadPositionAndFile()
                            self.media_index = fileAndPosition['fileIndex']
                            self.media_position = fileAndPosition['position']
                            self.PlayMediaFile()
                        else:
                            self.player.PlayPause()
                    if event.key == pygame.K_u :
                        print("volume +")
                        self.player.VolumeUp()
                    if event.key == pygame.K_d :
                        print("volume -")
                        self.player.VolumeDown()
                    if event.key == pygame.K_LEFT :
                        print("left")
                        if self.albumMode:
                            if self.album_index > 0:
                                self.album_index -= 1
                            self.ShowAlbums()
                        else:
                            if self.media_index > 0:
                                self.media_index -= 1
                                self.PlayMediaFile()
                    if event.key == pygame.K_RIGHT :
                        print("rigth")
                        if self.albumMode:
                            if self.album_index < len(self.folders) - 1:
                                self.album_index += 1
                            self.ShowAlbums()
                        else:
                            size = self.repo.GetNumberOfFiles(self.folders[self.album_index])
                            if self.media_index + 1 < size:
                                self.media_index += 1
                                self.PlayMediaFile()
            clock.tick(30)
            self.SavePosition()

    def PlayMediaFile(self):
        fileName = self.repo.GetFiles(self.folders[self.album_index])[self.media_index]
        meta = self.repo.GetInfo(fileName)
        image = self.repo.GetCover(self.folders[self.album_index])
        self.view.NewMedia(image, meta.title, meta.artist, meta.album, meta.track, 0, self.media_position)
        self.player.SetFile(fileName, self.media_position)
        self.albumMode = False

    def SavePosition(self):
        if self.player.IsPlaying() :
            if time.time() > self.lastUpdate:
                folder = self.folders[self.album_index]
                self.media_position = self.player.GetPosition()
                with open(self.rootFolder + "\\" + folder + "\\" + "position.json", "w") as write_file:
                    data = {
                        "fileIndex": self.media_index,
                        "position": self.media_position
                    }
                    json.dump(data, write_file)
                self.lastUpdate = time.time()
    
    def LoadPositionAndFile(self):
        try:
            with open(self.rootFolder + "\\" + self.folders[self.album_index] + "\\" + "position.json", "r") as read_file:
                return json.load(read_file)
        except:
            self.media_index = 0
            self.media_position = 0.0
            return {
                        "fileIndex": 0,
                        "position": 0
                    }


    def ShowAlbums(self):
        centerIndex = self.album_index

        if centerIndex - 1 < 0:
            image1 = self.noCoverImage
        else:
            image1 = self.repo.GetCover(self.folders[centerIndex -1])

        image2 = self.repo.GetCover(self.folders[centerIndex])

        if centerIndex + 1 > len(self.folders) - 1:
            image3 = self.noCoverImage
        else:
            image3 = self.repo.GetCover(self.folders[centerIndex + 1])

        self.view.AlbumSelection(image1, image2, image3)