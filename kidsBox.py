import pygame
import os
import sys, signal
import vlc
from time import sleep

#os.environ["SDL_FBDEV"] = "/dev/fb1"

pygame.display.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('Some Text', False, (0, 0, 0))

#screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
screen = pygame.display.set_mode((480, 320))
screen.fill((100,100,100))

pygame.display.update()

#sleep(5)

instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new("rise.mp3")
player.set_media(media)
player.play()

pygame.mouse.set_visible(False)
pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(0, 0, 160, 160))
pygame.draw.rect(screen, (255, 128, 255), pygame.Rect(200, 0, 20, 20))

screen.blit(textsurface,(10,10))
pygame.display.flip()


player.audio_set_volume(100)
sleep(5)

player.set_position(0.5)

sleep(1)
player.audio_set_volume(95)
sleep(1)
player.audio_set_volume(90)
sleep(1)
textsurface = myfont.render(str(player.get_position() * 1000), False, (200, 200, 0))
screen.blit(textsurface,(10,160))
pygame.display.flip()

player.audio_set_volume(85)
sleep(1)
player.audio_set_volume(80)
sleep(1)
player.audio_set_volume(75)
sleep(1)
player.audio_set_volume(70)
sleep(1)
player.audio_set_volume(65)
sleep(1)
player.audio_set_volume(60)
sleep(1)
player.audio_set_volume(55)
sleep(1)
player.audio_set_volume(50)
sleep(10)
player.stop()

pygame.quit()
sys.exit(0)

#done = False

#while not done:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            done = True
#
#        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(0, 0, 160, 160))
#        pygame.draw.rect(screen, (255, 128, 255), pygame.Rect(200, 0, 20, 20))
#        pygame.display.flip()
