import pygame
import sys, signal
import vlc
import time
import platform

from Player import Player
from View import View
from MusicRepo import MusicRepo
from time import sleep

if platform.system() != 'Windows':
    from buttons import Buttons

class Controller:
    def __init__(self, display):
        self.display = display
        self.view = View(self.display)
        self.album_index = 0
        self.album_selected_index = 0
        self.media_index = 0
        self.media_position = 0.0
        self.media_duration = 0.0
        self.lastUpdate = 0.0
        self.keyDownTime = time.time()
        self.albumMode = True
        if platform.system() != 'Windows':
            self.rootFolder = "/home/pi/media"
        else:
            self.rootFolder = "C:\\Users\\nerv\\sandbox"
        self.busy = False
        self.lastChannel = -1
        if platform.system() != 'Windows':
            self.buttons = Buttons()

    def setup(self):
        self.view.Welcome()
        self.vlcInstance = vlc.Instance()
        self.player = Player(self.vlcInstance)
        self.player.Volume(60)

        self.player.set_event_end_callback(self.media_end_reached)
        self.player.set_event_position_changed_callback(self.media_position_changed)
        self.repo = MusicRepo(self.rootFolder, self.vlcInstance)
        self.repo.LoadAll()
        self.folders = self.repo.GetAlbums()
        if platform.system() != 'Windows':
            self.buttons.start_thread()

    def media_end_reached(self, event):
        #print("end reached")
        event = pygame.event.Event(pygame.KEYUP)
        event.key = pygame.K_RIGHT
        event.fileend = True
        pygame.event.post(event)
    
    def media_position_changed(self, event):
        #print("position changed")  
        event = pygame.event.Event(pygame.KEYUP)
        event.key = pygame.K_s
        pygame.event.post(event)

    def loop(self):
        self.ShowAlbums()
        while True:
            try:
                for event in pygame.event.get():
                    pygame.event.clear()
                    if event.type == pygame.QUIT:
                        self.run = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        self.keyDownTime = time.time()

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_q :
                            pygame.quit()
                            sys.exit(0)
                        elif event.key == pygame.K_s :
                            self.SavePosition()
                        elif event.key == pygame.K_ESCAPE :
                            #print("back")
                            self.albumMode = True
                            self.ShowAlbums()
                        elif event.key == pygame.K_p :
                            #print("enter / play-pause")
                            if time.time() > self.keyDownTime + 1:
                                if not self.albumMode:
                                    #print("reset")
                                    self.media_position = 0
                                    self.PlayMediaFile()
                            else: 
                                if self.albumMode:
                                    #print("open album")
                                    self.album_index = self.album_selected_index
                                    fileAndPosition = self.repo.LoadPositionAndFile(self.album_index)
                                    self.media_index = fileAndPosition['fileIndex']
                                    self.media_position = fileAndPosition['position']
                                    self.PlayMediaFile()
                                else:
                                    #print("toggle play")
                                    self.player.PlayPause()
                        elif event.key == pygame.K_UP :
                            #print("volume +")
                            self.player.VolumeUp()
                        elif event.key == pygame.K_DOWN :
                            #print("volume -")
                            self.player.VolumeDown()
                        elif event.key == pygame.K_LEFT :
                            #print("left")
                            if self.albumMode:
                                if self.album_selected_index > 0:
                                    self.album_selected_index -= 1
                                self.ShowAlbums()
                            else:
                                if self.media_index > 0:
                                    self.media_index -= 1
                                    self.media_position = 0
                                    self.PlayMediaFile()
                        elif event.key == pygame.K_RIGHT :
                            #print("right")
                            if self.albumMode:
                                if self.album_selected_index < len(self.folders) - 1:
                                    self.album_selected_index += 1
                                self.ShowAlbums()
                            else:
                                self.NextMediaFile(event)
            except:
                print("Failed")
                self.buttons.close()
                return
                

    def NextMediaFile(self, event):
        size = self.repo.GetNumberOfFiles(self.folders[self.album_index])
        if self.media_index + 1 < size:
            self.media_position = 0
            self.media_index += 1
            self.PlayMediaFile()
        elif hasattr(event, 'fileend'):
            self.media_position = 0
            self.media_index = 0
            self.SavePosition()
            self.ShowAlbums()

    def PlayMediaFile(self):
        files = self.repo.get_mediafiles(self.folders[self.album_index])
        meta = files[self.media_index]
        image = self.repo.GetCover(self.folders[self.album_index])
        self.media_duration = meta.duration
        if self.media_position > 1.0:
            self.media_position = 0
        self.view.NewMedia(image, meta.title, meta.artist, meta.album, meta.track, meta.duration, self.media_position)
        self.player.SetFile(meta.filename, self.media_position)
        self.albumMode = False

    def SavePosition(self):
        if self.player.IsPlaying() :
            if time.time() > self.lastUpdate + 1:
                self.media_position = self.player.GetPosition()
                if not self.albumMode:
                    self.view.DrawPositionBar(self.media_position, self.media_duration)
                self.repo.SavePosition(self.album_index, self.media_index, self.media_position)
                self.lastUpdate = time.time()


    def ShowAlbums(self):
        centerIndex = self.album_selected_index

        if centerIndex - 1 < 0:
            image1 = None
        else:
            image1 = self.repo.GetCover(self.folders[centerIndex -1])

        image2 = self.repo.GetCover(self.folders[centerIndex])

        if centerIndex + 1 > len(self.folders) - 1:
            image3 = None
        else:
            image3 = self.repo.GetCover(self.folders[centerIndex + 1])

        self.view.AlbumSelection(image1, image2, image3)

