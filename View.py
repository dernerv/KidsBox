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

    def NewMedia(self, image, titel, album, track, position, fulltime):
        self.image = image
        self.titel = titel
        self.position = position
        
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, 0, self.display.get_width(), self.display.get_height()-60))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(9, 9, 242, 242))
        
        # Cover
        picture = pygame.transform.smoothscale(image, (240, 240))
        self.display.blit(picture,(10,10))
        # Track
        textTitel = self.fontSmall.render("#" + str(track), True, (200, 200, 200))
        self.display.blit(textTitel,(270,80))
        # Titel
        textTitel = self.fontSmall.render(titel, True, (200, 200, 200))
        self.display.blit(textTitel,(270,110))
        # Album
        textTitel = self.fontSmall.render(album, True, (200, 200, 200))
        self.display.blit(textTitel,(270,140))

        pygame.display.flip()
        self.DrawPositionBar(position, fulltime)
    
    def DrawPositionBar(self, position, fulltime):
        pygame.draw.rect(self.display, (100, 100, 100), pygame.Rect(0, self.display.get_height()-60, self.display.get_width(), 60))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(20, self.display.get_height()-50, self.display.get_width()-40, 40))
        pygame.display.flip()

    def UpdateTitle(self, titel, position):
        self.titel = titel
        self.position = position

    def UpdatePosition(self, position):
        self.position = position 

    def ShowVolume(self, volume):
        self.volume = volume
    
