import pygame
import sys, signal
import vlc
import time
import platform

from player import Player
from view import View
from musicRepo import MusicRepo
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
            self.buttons = buttons()

    def setup(self):
        self.view.welcome()
        self.vlcInstance = vlc.Instance()
        self.player = Player(self.vlcInstance)
        self.player.volume(60)

        self.player.set_event_end_callback(self.media_end_reached)
        self.player.set_event_position_changed_callback(self.media_position_changed)
        self.repo = MusicRepo(self.rootFolder, self.vlcInstance)
        self.repo.load_all()
        self.folders = self.repo.get_albums()
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
        self.show_albums()
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
                            self.save_position()
                        elif event.key == pygame.K_ESCAPE :
                            #print("back")
                            self.albumMode = True
                            self.show_albums()
                        elif event.key == pygame.K_p :
                            #print("enter / play-pause")
                            if time.time() > self.keyDownTime + 1:
                                if not self.albumMode:
                                    #print("reset")
                                    self.media_position = 0
                                    self.play_media_file()
                            else: 
                                if self.albumMode:
                                    #print("open album")
                                    self.album_index = self.album_selected_index
                                    fileAndPosition = self.repo.load_position_and_file(self.album_index)
                                    self.media_index = fileAndPosition['fileIndex']
                                    self.media_position = fileAndPosition['position']
                                    self.play_media_file()
                                else:
                                    #print("toggle play")
                                    self.player.play_pause()
                        elif event.key == pygame.K_UP :
                            #print("volume +")
                            self.player.volume_up()
                        elif event.key == pygame.K_DOWN :
                            #print("volume -")
                            self.player.volume_down()
                        elif event.key == pygame.K_LEFT :
                            #print("left")
                            if self.albumMode:
                                if self.album_selected_index > 0:
                                    self.album_selected_index -= 1
                                self.show_albums()
                            else:
                                if self.media_index > 0:
                                    self.media_index -= 1
                                    self.media_position = 0
                                    self.play_media_file()
                        elif event.key == pygame.K_RIGHT :
                            #print("right")
                            if self.albumMode:
                                if self.album_selected_index < len(self.folders) - 1:
                                    self.album_selected_index += 1
                                self.show_albums()
                            else:
                                self.next_media_file(event)
            except:
                print("Failed")
                self.buttons.close()
                return
                

    def next_media_file(self, event):
        size = self.repo.get_num_of_files(self.folders[self.album_index])
        if self.media_index + 1 < size:
            self.media_position = 0
            self.media_index += 1
            self.play_media_file()
        elif hasattr(event, 'fileend'):
            self.media_position = 0
            self.media_index = 0
            self.save_position()
            self.show_albums()

    def play_media_file(self):
        files = self.repo.get_mediafiles(self.folders[self.album_index])
        meta = files[self.media_index]
        image = self.repo.get_cover(self.folders[self.album_index])
        self.media_duration = meta.duration
        if self.media_position > 1.0:
            self.media_position = 0
        self.view.new_media(image, meta.title, meta.artist, meta.album, meta.track, meta.duration, self.media_position)
        self.player.set_file(meta.filename, self.media_position)
        self.albumMode = False

    def save_position(self):
        if self.player.is_playing() :
            if time.time() > self.lastUpdate + 1:
                self.media_position = self.player.get_position()
                if not self.albumMode:
                    self.view.draw_position_bar(self.media_position, self.media_duration)
                self.repo.save_position(self.album_index, self.media_index, self.media_position)
                self.lastUpdate = time.time()


    def show_albums(self):
        centerIndex = self.album_selected_index

        if centerIndex - 1 < 0:
            image1 = None
        else:
            image1 = self.repo.get_cover(self.folders[centerIndex -1])

        image2 = self.repo.get_cover(self.folders[centerIndex])

        if centerIndex + 1 > len(self.folders) - 1:
            image3 = None
        else:
            image3 = self.repo.get_cover(self.folders[centerIndex + 1])

        self.view.album_selection(image1, image2, image3)

