#! /usr/bin/python

import pygame
import os
import platform

from controller import Controller

def main():
    if platform.system() != 'Windows':
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        display = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode((480, 320))
        pygame.display.set_caption('KidsBox')
    pygame.mouse.set_visible(False)
    
    print("starting KidBox 1.1")
    control = Controller(display)
    control.setup()
    control.loop()
    pygame.quit()

if __name__ == '__main__':
    main()