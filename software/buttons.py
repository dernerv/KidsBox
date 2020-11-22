import pygame
import RPi.GPIO as GPIO

from time import sleep
from threading import Thread

## Buttons
BACK_BUTTON = 5
PLAY_BUTTON = 20
LEFT_BUTTON = 12
RIGHT_BUTTON = 16

VOLUME_UP = 13
VOLUME_DOWN = 6

BUTTON_LIST = {BACK_BUTTON, PLAY_BUTTON, LEFT_BUTTON, RIGHT_BUTTON, VOLUME_UP, VOLUME_DOWN}

class Buttons:
    # def Interrupt(channel):
    #     for button in BUTTON_LIST:
    #         if button == channel:
    #             #print("Button up " + str(button))
    #             event = pygame.event.Event(pygame.KEYUP)
    #             if button == PLAY_BUTTON:  
    #                 event.key = pygame.K_p
    #             elif button == LEFT_BUTTON:  
    #                 event.key = pygame.K_LEFT
    #             elif button == RIGHT_BUTTON:  
    #                 event.key = pygame.K_RIGHT
    #             elif button == BACK_BUTTON:  
    #                 event.key = pygame.K_ESCAPE
    #             elif button == VOLUME_UP:  
    #                 event.key = pygame.K_UP
    #             elif button == VOLUME_DOWN:  
    #                 event.key = pygame.K_DOWN
    #             pygame.event.post(event)
        

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for button in BUTTON_LIST:
            GPIO.setup(button, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
           # GPIO.add_event_detect(18, GPIO.RISING, callback = Interrupt, bouncetime = 250) 
    
    def start_thread(self):
        self.run = True
        self.thread = Thread(target = self.checkButtons)
        self.thread.start()

    def close(self):
        self.run = False

    def checkButtons(self):
        ##print("gpio is high " + str(channel))
        channel = -1
        while self.run:
            #event = pygame.event.Event(pygame.KEYUP)
            for button in BUTTON_LIST:
                if GPIO.input(button) == False and channel != button:
                    #print("Button down " + str(button))
                    channel = button
                    event = pygame.event.Event(pygame.KEYDOWN)
                    pygame.event.post(event)
                    sleep(0.1)

            for button in BUTTON_LIST:
                if button == channel and GPIO.input(button):
                    #print("Button up " + str(button))
                    event = pygame.event.Event(pygame.KEYUP)
                    if button == PLAY_BUTTON:  
                        event.key = pygame.K_p
                    elif button == LEFT_BUTTON:  
                        event.key = pygame.K_LEFT
                    elif button == RIGHT_BUTTON:  
                        event.key = pygame.K_RIGHT
                    elif button == BACK_BUTTON:  
                        event.key = pygame.K_ESCAPE
                    elif button == VOLUME_UP:  
                        event.key = pygame.K_UP
                    elif button == VOLUME_DOWN:  
                        event.key = pygame.K_DOWN
                    pygame.event.post(event)
                    channel = -1
            sleep(0.05)