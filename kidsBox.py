import pygame

from controller import Controller

def main():
    display = pygame.display.set_mode((800,600))
    pygame.display.set_caption('test')

    control = Controller(display)
    control.loop()

if __name__ == '__main__':
    main()