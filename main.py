import sys
import pygame

import mario
import coinbox
import config
import tmx

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class MarioGame(object):

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
        self.tilemap = tmx.load('map.tmx', self.screen.get_size())
        start_cell = self.tilemap.layers['triggers'].find('player')[0]

        self.sprites = tmx.SpriteLayer()
        self.my_mario = mario.Mario(self.sprites)
        self.my_mario.set_position(start_cell.px, start_cell.py)

        self.coinboxs = tmx.SpriteLayer()
        for _coinbox in self.tilemap.layers['triggers'].find('coinbox'):
            coinbox.CoinBox((_coinbox.px, _coinbox.py), coinbox.SECRET, self.coinboxs)

        self.tilemap.layers.add_named(self.sprites, "sprites")
        self.tilemap.layers.add_named(self.coinboxs, "coinboxs")

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

            self.tilemap.update(dt / 1000., self)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill(config.SKY)
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Hello World !", 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.width/2)
            self.screen.blit(text, textpos)
        # TODO: sprite draw
        self.tilemap.draw(screen)
        self.pygame.display.flip()

    def update(self):
        self.my_mario.update()

    def handle(self, event):
        self.my_mario.handle(event)

if __name__ == '__main__':
    g = MarioGame()
    g.init()
    g.run()
