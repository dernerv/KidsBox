#! /usr/bin/python
import version
import pygame
import os
import platform

from controller import Controller



def main():
    if 'arm' in platform.processor():
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        display = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode((480, 320))
        pygame.display.set_caption('KidsBox')
    pygame.mouse.set_visible(False)
    
    print("starting KidBox " + version.__version__)
    control = Controller(display)
    control.setup()
    control.loop()
    pygame.quit()

if __name__ == '__main__':
    main()