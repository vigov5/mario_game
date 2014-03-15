import sys
import pygame

import mario
import coinbox
import brick
import flower
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
        self.init_map('map.tmx', None, True)
        self.bg_color = config.SKY

    def init_map(self, map_file, new_pos, first_time):
        self.tilemap = tmx.load(map_file, self.screen.get_size())

        if first_time:
            self.sprites = tmx.SpriteLayer()
            self.my_mario = mario.Mario(self.sprites)
            start_cell = self.tilemap.layers['triggers'].find('player')[0]
        else:
            start_cell = self.tilemap.layers['triggers'].find(new_pos)[0]
        self.my_mario.set_position(start_cell.px, start_cell.py)

        self.coinboxs = tmx.SpriteLayer()
        for _coinbox in self.tilemap.layers['triggers'].find('coinbox'):
            box_type = getattr(coinbox, _coinbox.properties.get("type", "SECRET"))
            count = _coinbox.properties.get("count", 1)
            coinbox.CoinBox(self, (_coinbox.px, _coinbox.py), box_type, count, self.coinboxs)

        self.bricks = tmx.SpriteLayer()
        for _brick in self.tilemap.layers['triggers'].find('brick'):
            brick.Brick(self, (_brick.px, _brick.py), self.bricks)

        self.flowers = tmx.SpriteLayer()
        for _flower in self.tilemap.layers['triggers'].find('flower'):
            color = getattr(flower, _flower.properties.get("color", "GREEN_FLOWER"))
            flower.Flower(self, (_flower.px, _flower.py), color, self.flowers)

        # layer order: background, midground + sprites, foreground
        self.insert_layer(self.sprites, "sprites", 1)
        self.insert_layer(self.coinboxs, "coinboxs", 2)
        self.insert_layer(self.bricks, "bricks", 3)
        self.insert_layer(self.flowers, "flowers", 4)

    def insert_layer(self, sprites, layer_name, z_order):
        self.tilemap.layers.add_named(sprites, layer_name)
        self.tilemap.layers.remove(sprites)
        self.tilemap.layers.insert(z_order, sprites)

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

            self.update(dt)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill(self.bg_color)
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Hello World !", 1, (255, 0, 0))
            textpos = text.get_rect(centerx=self.width/2)
            self.screen.blit(text, textpos)
        # TODO: sprite draw
        for box in self.coinboxs:
            box.draw_coin(screen)
        self.tilemap.draw(screen)
        for brick in self.bricks:
            brick.draw_particles(screen)
        #self.draw_debug(screen)
        self.pygame.display.flip()

    def draw_debug(self, screen):
        pygame.draw.rect(screen,  config.WHITE, pygame.Rect(260, 368, 20, 14))

    def update(self, dt):
        if self.my_mario.state == "piped":
            next_map = self.my_mario.pipe_obj.properties.get("map")
            new_pos = self.my_mario.pipe_obj.properties.get("next")
            self.init_map(next_map + '.tmx', new_pos, False)
            if "underground" in next_map:
                self.bg_color = config.BLACK
            else:
                self.bg_color = config.SKY
            self.my_mario.state = "normal"

        self.tilemap.update(dt / 1000., self)

    def handle(self, event):
        self.my_mario.handle(event)

if __name__ == '__main__':
    g = MarioGame()
    g.init()
    g.run()
