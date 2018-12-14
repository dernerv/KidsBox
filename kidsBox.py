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

    control = Controller(display)
    control.loop()

if __name__ == '__main__':
    main()