#! /usr/bin/python
# -*- coding: utf-8 -*-
import version
import pygame
import os
import platform

from controller import Controller

def main():
    print("starting KidBox " + version.__version__ + "\n")
    print("platform: ")
    if 'arm' in platform.machine():
        print('arm')
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        display = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    else:
        print('not arm')
        display = pygame.display.set_mode((480, 320))
        pygame.display.set_caption('KidsBox')
    pygame.mouse.set_visible(False)

    control = Controller(display)
    control.setup()
    control.loop()
    pygame.quit()

if __name__ == '__main__':
    main()
