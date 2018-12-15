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
        
    def loop(self):
        clock = pygame.time.Clock()
        print(self.repo.GetSubFolders())

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s :
                        print("play file")
                        filename = "chemie.mp3"
                        self.player.SetFile(filename, 0.4)
                        meta = self.repo.GetInfo(filename)
                        image = self.repo.GetCover(self.repo.GetSubFolders()[1])
                        self.view.NewMedia(image, meta.title, meta.artist, meta.album, meta.track, 0, 3.5)
                    if event.key == pygame.K_p :
                        print("play / pause")
                    if event.key == pygame.K_a :
                        print("album")
                        image1 = self.repo.GetCover(self.repo.GetSubFolders()[0])
                        image2 = self.repo.GetCover(self.repo.GetSubFolders()[1])
                        image3 = self.repo.GetCover(self.repo.GetSubFolders()[2])
                        self.view.AlbumSelection(image1, image2, image3)
                    if event.key == pygame.K_u :
                        print("volume +")
                        self.player.VolumeUp()
                    if event.key == pygame.K_d :
                        print("volume -")
                        self.player.VolumeDown()
                #print(event)
            #pygame.display.update()
            clock.tick(30)
        #pygame.display.update()
        #clock.tick(30)