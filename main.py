import sys
import pygame
import tmx

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class MarioGame():

    width = 640
    height = 480

    def __init__(self):
        self.pygame = pygame

    def init(self):
        self.pygame.init()
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = self.pygame.time.Clock()
        self.time_step = 0
        # TODO: init sprite, tile,...
        self.tilemap = tmx.load("map.tmx", self.screen.get_size())

    def run(self):
        # main game loop
        while True:
            # hold frame rate at 60 fps
            dt = self.clock.tick(60)
            self.time_step += 1
            # enumerate event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # sprite handle event
                self.handle(event)

            self.update(dt / 1000.)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill((95, 183, 229)) # sky color
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Hello World !", 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.width/2)
            self.screen.blit(text, textpos)
        # TODO: sprite tilemap
        self.tilemap.set_focus(0, 480)
        self.tilemap.draw(screen)
        self.pygame.display.flip()

    def update(self, dt):
        #self.mariosprite.update()
        pass

    def handle(self, event):
        #self.my_mario.handle(event)
        pass

if __name__ == '__main__':
    g = MarioGame()
    g.init()
    g.run()
