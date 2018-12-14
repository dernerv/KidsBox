import pygame

class View:

    def __init__(self, display):
        self.display = display
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.font = pygame.font.SysFont('Century Gothic', 30) 
    
    def Welcome(self):
        textsurface = self.font.render('Kids Box v1.0', True, (200, 200, 200))
        self.display.fill((0,0,0))
        self.display.blit(textsurface,(40,160))
        
        pygame.display.flip()

    def NewMedia(self, image, titel, position):
        self.image = image
        self.titel = titel
        self.position = position
    
    def UpdateTitle(self, titel, position):
        self.titel = titel
        self.position = position

    def UpdatePosition(self, position):
        self.position = position 

    def ShowVolume(self, volume):
        self.volume = volume
    
