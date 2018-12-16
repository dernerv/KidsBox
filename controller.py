import pygame
import sys, signal
import vlc

from Player import Player
from View import View
from time import sleep
from MusicRepo import MusicRepo

class Controller:
    def __init__(self, display):
        self.display = display
        self.vlcInstance = vlc.Instance()
        self.player = Player(self.vlcInstance)
        self.view = View(self.display)
        self.view.Welcome()
        self.repo = MusicRepo("C:\\Users\\nerv\\sandbox", self.vlcInstance)
        self.folders = self.repo.GetSubFolders()
        self.index = 0
        self.noCoverImage = pygame.image.load("no-cover.png")
        self.albumMode = True
        
    def loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE :
                        print("back")
                        self.albumMode = True
                        self.ShowAlbums()
                    if event.key == pygame.K_p :
                        print("enter / play-pause")
                        if self.albumMode:
                            fileName = self.repo.GetFiles(self.folders[self.index])[0]
                            lastPosition = 0
                            meta = self.repo.GetInfo(fileName)
                            image = self.repo.GetCover(self.folders[self.index])
                            self.view.NewMedia(image, meta.title, meta.artist, meta.album, meta.track, 0, lastPosition)
                            self.player.SetFile(fileName, lastPosition)
                            self.albumMode = False
                        else:
                            self.player.PlayPause()
                    if event.key == pygame.K_a :
                        print("album")
                        image1 = self.repo.GetCover(self.folders[1])
                        image2 = self.repo.GetCover(self.folders[2])
                        image3 = self.repo.GetCover(self.folders[3])
                        self.view.AlbumSelection(image1, image2, image3)
                    if event.key == pygame.K_u :
                        print("volume +")
                        self.player.VolumeUp()
                    if event.key == pygame.K_d :
                        print("volume -")
                        self.player.VolumeDown()
                    if event.key == pygame.K_LEFT :
                        print("left")
                        if self.albumMode:
                            if self.index > 0:
                                self.index -= 1
                            self.ShowAlbums()
                    if event.key == pygame.K_RIGHT :
                        print("rigth")
                        if self.albumMode:
                            if self.index < len(self.folders) - 1:
                                self.index += 1
                            self.ShowAlbums()
            clock.tick(30)

    def ShowAlbums(self):
        centerIndex = self.index

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