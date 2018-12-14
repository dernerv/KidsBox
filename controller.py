import pygame
import sys, signal

from Player import Player
from View import View
from time import sleep

class Controller:
    def __init__(self, display):
        self.display = display
        self.player = Player()
        self.view = View(self.display)
        self.view.Welcome()
        
    def loop(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s :
                        print("play file")
                        self.player.PlayFile("rise.mp3", 0.4)
                        image = pygame.image.load("C:\\Users\\nerv\\sandbox\\Album1\\cover.png")
                        self.view.NewMedia(image, "Test Titel", 0)
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