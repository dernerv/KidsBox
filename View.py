import pygame

class View:

    def __init__(self, display):
        self.display = display
        self.margin = 10
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.font = pygame.font.SysFont('Century Gothic', 40)
        self.fontSmall = pygame.font.SysFont('Century Gothic', 16) 
        self.frameColor = (255, 255, 255)
    
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

    def NewMedia(self, image, titel, artist, album, track, position, fulltime):
        self.image = image
        self.titel = titel
        self.position = position
        self.artist = artist
        
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, 0, self.display.get_width(), self.display.get_height()-60))
        pygame.draw.rect(self.display, self.frameColor, pygame.Rect(9, 9, 242, 242))
        
        # Cover
        picture = pygame.transform.smoothscale(image, (240, 240))
        self.display.blit(picture,(10,10))
        # Track
        textTitel = self.fontSmall.render("#" + str(track), True, (200, 200, 200))
        self.display.blit(textTitel,(270,70))
        # Titel
        textTitel = self.fontSmall.render(titel, True, (200, 200, 200))
        self.display.blit(textTitel,(270,100))
        # Artits
        textTitel = self.fontSmall.render(artist, True, (200, 200, 200))
        self.display.blit(textTitel,(270,130))
        # Album
        textTitel = self.fontSmall.render(album, True, (200, 200, 200))
        self.display.blit(textTitel,(270,160))

        pygame.display.flip()
        self.DrawPositionBar(position, fulltime)
    
    def DrawPositionBar(self, position, fulltime):
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, self.display.get_height()-60, self.display.get_width(), 60))
        pygame.draw.rect(self.display, (100, 100, 100), pygame.Rect(15, self.display.get_height()-45, self.display.get_width()-30, 30))
        
        # Progress position
        if position <= 1.0:
            pygame.draw.rect(self.display, (20, 20, 200), pygame.Rect(15, self.display.get_height()-45, (self.display.get_width()-30) * position , 30))

        durationInSec = fulltime / 60000
        position_in_sec =  durationInSec * position 
        position_as_time_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(position_in_sec * 60, 60))
        positionText = self.fontSmall.render(position_as_time_format, True, (200, 200, 200))
        self.display.blit(positionText,(20, self.display.get_height()-40))

        duration_as_time_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(durationInSec * 60, 60))
        fulltimeText = self.fontSmall.render(duration_as_time_format, True, (200, 200, 200))
        self.display.blit(fulltimeText,(self.display.get_width()- (fulltimeText.get_width() + 20), self.display.get_height()-40))
        pygame.display.flip()

    def UpdateTitle(self, titel, position):
        self.titel = titel
        self.position = position

    def UpdatePosition(self, position):
        self.position = position 

    def ShowVolume(self, volume):
        self.volume = volume
    
    def AlbumSelection(self, image1, image2, image3):
        self.display.fill((0,0,0))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, 0, self.display.get_width(), self.display.get_height()-60))
        
        coverSize = 220
        frameSize = coverSize + 2
        centerX = self.display.get_width() / 2
        # Cover
        pygame.draw.rect(self.display, self.frameColor, pygame.Rect(9, 9, frameSize, frameSize))
        picture = pygame.transform.smoothscale(image1, (coverSize, coverSize))
        self.display.blit(picture,(10,10))
       
        pygame.draw.rect(self.display, self.frameColor, pygame.Rect(249, 9, frameSize, frameSize))
        picture = pygame.transform.smoothscale(image3, (coverSize, coverSize))
        self.display.blit(picture,(250,10))

        centerCoverSize = coverSize + 40
        centerFrame = centerCoverSize + 2
        pygame.draw.rect(self.display, self.frameColor, pygame.Rect(108, 39, centerFrame, centerFrame))
        picture = pygame.transform.smoothscale(image2, (centerCoverSize, centerCoverSize))
        self.display.blit(picture,(109,40))

        pygame.display.flip()