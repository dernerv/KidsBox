import pygame

class View:

    def __init__(self, display):
        self.display = display
        self.margin = 10
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.font = pygame.font.SysFont('Century Gothic', 40)
        self.fontSmall = pygame.font.SysFont('Century Gothic', 16) 
    
    def Welcome(self):
        textKidsBox = self.font.render('Kids Box', True, (255, 255, 255))
        textVersion = self.fontSmall.render('Version 1.0', True, (150, 150, 150))
        self.display.fill((0,0,0))

        centerX = self.display.get_width() / 2
        centerY = self.display.get_height() / 2

        # Render KidsBox
        startKidTextX = (centerX- textKidsBox.get_width()/2)
        startKidTextY = (centerY- textKidsBox.get_height()/2) - 20
        self.display.blit(textKidsBox, (startKidTextX, startKidTextY))

        #Render Version
        startVersionTextX = (textKidsBox.get_width() - textVersion.get_width()) + startKidTextX
        startVersionTextY = startKidTextY + textKidsBox.get_height()
        self.display.blit(textVersion,(startVersionTextX,startVersionTextY))

        pygame.display.flip()

    def NewMedia(self, image, titel, position):
        self.image = image
        self.titel = titel
        self.position = position
        
        self.display.fill((110,110,110))
        picture = pygame.transform.smoothscale(image, (300, 300))
        self.display.blit(picture,(10,10))
        textTitel = self.fontSmall.render(self.titel, True, (150, 150, 150))
        self.display.blit(textTitel,(320,10))
        pygame.display.flip()
    
    def UpdateTitle(self, titel, position):
        self.titel = titel
        self.position = position

    def UpdatePosition(self, position):
        self.position = position 

    def ShowVolume(self, volume):
        self.volume = volume
    
