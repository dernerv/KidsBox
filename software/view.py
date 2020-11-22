import version
import sys, os
import pygame
from PIL import Image

COVER_POSITION_X = 10
COVER_POSITION_Y = 10

class View:

    def __init__(self, display):
        self.display = display
        self.margin = 10
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        fontname = 'Century Gothic' #'Century Gothic' ' Staatliches', 'Didact Gothic'
        self.font = pygame.font.SysFont(fontname, 45)
        self.fontSmall = pygame.font.SysFont(fontname, 20) 
        self.frameColor = (255, 255, 255)
        self.picture_cache_220 = dict()
        self.picture_cache_260 = dict()
        self.showAlbum = False
    
    def welcome(self):
        textKidsBox = self.font.render('Kids Box', True, (255, 255, 255))
        textVersion = self.fontSmall.render('Version ' + version.__version__, True, (150, 150, 150))
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

    def new_media(self, image, titel, artist, album, track, position, fulltime):
        self.image = image
        self.titel = titel
        self.position = position
        self.artist = artist
        self.showAlbum = False

        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, 0, self.display.get_width(), self.display.get_height()-60))
        pygame.draw.rect(self.display, self.frameColor, pygame.Rect(COVER_POSITION_X-1, COVER_POSITION_Y-1, 262, 262))
        
        # Cover
        picture = self.get_from_cache(image, 260)
        self.display.blit(picture,(COVER_POSITION_X, COVER_POSITION_Y))
        # Track
        textTitel = self.fontSmall.render("#" + str(track), True, (200, 200, 200))
        self.display.blit(textTitel,(280,70))
        # Titel
        textTitel = self.fontSmall.render(titel, True, (200, 200, 200))
        self.display.blit(textTitel,(280,100))
        # Artits
        textTitel = self.fontSmall.render(artist, True, (200, 200, 200))
        self.display.blit(textTitel,(280,130))
        # Album
        textTitel = self.fontSmall.render(album, True, (200, 200, 200))
        self.display.blit(textTitel,(280,160))

        pygame.display.flip()
        self.draw_position_bar(position, fulltime)
    
    def draw_position_bar(self, position, fulltime):
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, self.display.get_height()-60, self.display.get_width(), 60))
        pygame.draw.rect(self.display, (100, 100, 100), pygame.Rect(10, self.display.get_height()-45, self.display.get_width()-30, 30))
        
        # Progress position
        if position <= 1.0:
            pygame.draw.rect(self.display, (20, 20, 200), pygame.Rect(10, self.display.get_height()-45, (self.display.get_width()-30) * position , 30))

        durationInSec = fulltime / 60000
        position_in_sec =  durationInSec * position 
        position_as_time_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(position_in_sec * 60, 60))
        positionText = self.fontSmall.render(position_as_time_format, True, (200, 200, 200))
        self.display.blit(positionText,(20, self.display.get_height()-40))

        duration_as_time_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(durationInSec * 60, 60))
        fulltimeText = self.fontSmall.render(duration_as_time_format, True, (200, 200, 200))
        self.display.blit(fulltimeText,(self.display.get_width()- (fulltimeText.get_width() + 20), self.display.get_height()-40))
        pygame.display.flip()

    def update_title(self, titel, position):
        self.titel = titel
        self.position = position

    def update_position(self, position):
        self.position = position 

    def show_volume(self, volume):
        self.volume = volume
    
    def album_selection(self, image1, image2, image3):
        if not self.showAlbum:
            self.display.fill((0,0,0))
            pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(0, 0, self.display.get_width(), self.display.get_height()-60))
        self.showAlbum = True

        coverSize = 220
        frameSize = coverSize + 2
        # Cover
        if image1 != None:
            pygame.draw.rect(self.display, self.frameColor, pygame.Rect(9, 9, frameSize, frameSize))
            #picture = pygame.transform.smoothscale(image1, (coverSize, coverSize))
            #picture = pygame.transform.scale(image1, (coverSize, coverSize))
            picture = self.get_from_cache(image1, coverSize)
            
            self.display.blit(picture,(10,10))

            s = pygame.Surface((220, 220))
            s.set_alpha(128)
            s.fill((0,0,0))
            self.display.blit(s,(10,10))
        else:
            pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(9, 9, frameSize, frameSize))
       
        if image3 != None:
            pygame.draw.rect(self.display, self.frameColor, pygame.Rect(249, 9, frameSize, frameSize))
            #picture = pygame.transform.smoothscale(image3, (coverSize, coverSize))
            #picture = pygame.transform.scale(image3, (coverSize, coverSize))
            picture = self.get_from_cache(image3, coverSize)

            self.display.blit(picture,(250,10))
            
            s = pygame.Surface((220, 220))
            s.set_alpha(128)
            s.fill((0,0,0))
            self.display.blit(s,(250,10))
        else:
            pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(249, 9, frameSize, frameSize))      
        centerCoverSize = 260
        centerFrame = centerCoverSize + 2
        pygame.draw.rect(self.display, self.frameColor, pygame.Rect(108, 39, centerFrame, centerFrame))
        #picture = pygame.transform.smoothscale(image2, (centerCoverSize, centerCoverSize))
        picture = self.get_from_cache(image2, centerCoverSize)
        self.display.blit(picture,(109,40))

        pygame.display.flip()

    def get_from_cache(self, image, size):
            if size == 220:
                if not (image in self.picture_cache_220):
                    path, filename = os.path.split(image)
                    cover220 = path + "/220" + filename
                    if (not os.path.exists(cover220)):
                        im = Image.open(image)
                        size = 220, 220
                        im.thumbnail(size, Image.ANTIALIAS)
                        im.save(cover220, "PNG")
                    self.picture_cache_220[image] = pygame.image.load(cover220)
                    #self.picture_cache_220[image] = pygame.transform.smoothscale(image, (size, size))
                return self.picture_cache_220[image]
            elif size == 260:
                if not (image in self.picture_cache_260):
                    path, filename = os.path.split(image)
                    cover260 = path + "/260" + filename
                    if (not os.path.exists(cover260)):
                        im = Image.open(image)
                        size = 260, 260
                        im.thumbnail(size, Image.ANTIALIAS)
                        im.save(cover260, "PNG")
                    self.picture_cache_260[image] = pygame.image.load(cover260)
                    #self.picture_cache_260[image] = pygame.transform.smoothscale(image, (size, size))
                return self.picture_cache_260[image]
