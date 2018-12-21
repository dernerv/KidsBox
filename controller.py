import pygame
import sys, signal
import vlc
import asyncio

import time
#import RPi.GPIO as GPIO

from Player import Player
from View import View
from MusicRepo import MusicRepo
from time import sleep


class Controller:
    def __init__(self, display):
        self.display = display
        self.view = View(self.display)
        self.album_index = 0
        self.media_index = 0
        self.media_position = 0.0
        self.media_duration = 0.0
        self.lastUpdate = 0.0
        self.keyDownTime = 0
        self.albumMode = True
        self.rootFolder = "C:\\Users\\nerv\\sandbox"
        self.ButtonPinPlay = 18
        self.busy = False

    def setup(self):
        self.view.Welcome()
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.ButtonPinPlay, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        self.vlcInstance = vlc.Instance()
        self.player = Player(self.vlcInstance)
        self.player.set_event_end_callback(self.media_end_reached)
        self.player.set_event_position_changed_callback(self.media_position_changed)
        self.repo = MusicRepo(self.rootFolder, self.vlcInstance)
        self.folders = self.repo.GetAlbums()
        self.noCoverImage = pygame.image.load("no-cover.png")

    def media_end_reached(self, event):
        print("end reached")
        event = pygame.event.Event(pygame.KEYUP)
        event.key = pygame.K_RIGHT
        pygame.event.post(event)
        #asyncio.create_task(self.NextMediaFile())
    
    def media_position_changed(self, event):
        print("position changed")  
        if not self.busy:
            self.SavePosition()

    def loop(self):
        self.ShowAlbums()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.keyDownTime = time.time()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q :
                        pygame.quit()
                        sys.exit(0)
                    if event.key == pygame.K_ESCAPE :
                        print("back")
                        self.albumMode = True
                        self.ShowAlbums()
                    if event.key == pygame.K_p :
                        print("enter / play-pause")
                        if time.time() > self.keyDownTime + 2:
                            if not self.albumMode:
                                self.media_position = 0
                                self.PlayMediaFile()
                        else: 
                            if self.albumMode:
                                fileAndPosition = self.repo.LoadPositionAndFile(self.album_index)
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
                                self.media_position = 0
                                self.PlayMediaFile()
                    if event.key == pygame.K_RIGHT :
                        print("rigth")
                        if self.albumMode:
                            if self.album_index < len(self.folders) - 1:
                                self.album_index += 1
                            self.ShowAlbums()
                        else:
                            self.NextMediaFile()

    def NextMediaFile(self):
        self.busy = True
        size = self.repo.GetNumberOfFiles(self.folders[self.album_index])
        if self.media_index + 1 < size:
            self.media_position = 0
            self.media_index += 1
            self.PlayMediaFile()

    def PlayMediaFile(self):
        self.busy = True
        fileName = self.repo.GetFiles(self.folders[self.album_index])[self.media_index]
        meta = self.repo.GetInfo(fileName)
        image = self.repo.GetCover(self.folders[self.album_index])
        self.media_duration = meta.duration
        self.view.NewMedia(image, meta.title, meta.artist, meta.album, meta.track, meta.duration, self.media_position)
        self.player.SetFile(fileName, self.media_position)
        self.albumMode = False
        self.busy = False

    def SavePosition(self):
        if self.player.IsPlaying() :
            if time.time() > self.lastUpdate:
                self.media_position = self.player.GetPosition()
                if not self.albumMode:
                    self.view.DrawPositionBar(self.media_position, self.media_duration)
                self.repo.SavePosition(self.album_index, self.media_index, self.media_position)
                self.lastUpdate = time.time()


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