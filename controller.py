import pygame 

class Controller:
    def __init__(self, display):
        self.display = display
        
    def loop(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                print(event)

        pygame.display.update()
        clock.tick(30)