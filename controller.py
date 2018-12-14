import pygame
import sys, signal

from Player import Player
from View import View
from time import sleep
from MusicRepo import MusicRepo

class Controller:
    def __init__(self, display):
        self.display = display
        self.player = Player()
        self.view = View(self.display)
        self.view.Welcome()
        self.repo = MusicRepo("C:\\Users\\nerv\\sandbox")
        
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
                        self.player.PlayFile("rise.mp3", 0.4)
                        image = self.repo.GetCover(self.repo.GetSubFolders()[1])
                        self.view.NewMedia(image, "Test Titel", "Album", 5, 0, 3.5)
                    if event.key == pygame.K_p :
                        print("play / pause")
                        self.player.PlayPause()
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