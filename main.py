import sys
import pygame

import mario
import coinbox
import coin
import brick
import flower
import config
import tmx
import turtle
import powerup

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class MarioGame(object):

    width = 640
    height = 480
    game_over = False

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
            start_cell = self.tilemap.layers['triggers'].find('player')[0]
            self.my_mario = mario.Mario((100, 100), self.sprites)
        else:
            start_cell = self.tilemap.layers['triggers'].find(new_pos)[0]
        self.my_mario.rect.topleft = (start_cell.px, start_cell.py)

        self.coinboxs = tmx.SpriteLayer()
        for _coinbox in self.tilemap.layers['triggers'].find('coinbox'):
            box_type = getattr(coinbox, _coinbox.properties.get("type", "SECRET"))
            prize = None
            if _coinbox.properties.get("item"):
                prize = getattr(powerup, _coinbox.properties.get("item"))
            count = _coinbox.properties.get("count", 1)
            coinbox.CoinBox(self, (_coinbox.px, _coinbox.py), box_type, prize, count, self.coinboxs)

        self.bricks = tmx.SpriteLayer()
        for _brick in self.tilemap.layers['triggers'].find('brick'):
            brick.Brick(self, (_brick.px, _brick.py), self.bricks)

        self.coins = tmx.SpriteLayer()
        for _coin in self.tilemap.layers['triggers'].find('coin'):
            coin.Coin((_coin.px, _coin.py), self.coins)

        self.enemies = tmx.SpriteLayer()
        for _turtle in self.tilemap.layers['triggers'].find('turtle'):
            turtle.Turtle((_turtle.px, _turtle.py), self.enemies)
        for _flower in self.tilemap.layers['triggers'].find('flower'):
            color = getattr(flower, _flower.properties.get("color", "GREEN_FLOWER"))
            flower.Flower((_flower.px, _flower.py), color, self.enemies)

        self.powerups = tmx.SpriteLayer()
        # layer order: background, midground + sprites, foreground
        self.insert_layer(self.powerups, "powerups", 1)
        self.insert_layer(self.coins, "coins", 2)
        self.insert_layer(self.coinboxs, "coinboxs", 3)
        self.insert_layer(self.bricks, "bricks", 4)
        self.insert_layer(self.enemies, "enemies", 5)
        self.insert_layer(self.sprites, "sprites", 6)


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
                if event.type == pygame.QUIT \
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit(0)
                # sprite handle event
                self.handle(event)

            self.update(dt)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill(self.bg_color)
        if not self.game_over:
            for box in self.coinboxs:
                box.draw_coin(screen)
            self.tilemap.draw(screen)
            for brick in self.bricks:
                brick.draw_particles(screen)
            #self.draw_debug(screen)
            self.draw_score_texts(screen)
            if self.my_mario.state == "dying":
                self.draw_dying_screen(screen)
        else:
            self.draw_gameover_screen(screen)

        self.pygame.display.flip()

    def draw_debug(self, screen):
        pygame.draw.rect(screen,  config.WHITE, pygame.Rect(80, 396, 20, 14))

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


    def draw_score_texts(self, screen):
        if pygame.font:
            lives_text = pygame.font.Font(None, 24).render("MARIO x %s" % self.my_mario.lives, 1, (255, 255, 255))
            coins_text = pygame.font.Font(None, 24).render("COINS x %s" % self.my_mario.collected_coins, 1, (255, 255, 255))
            over_textpos = lives_text.get_rect(left=10, top=10)
            coins_textpos = coins_text.get_rect(right=self.width - 10, top=10)
            self.screen.blit(lives_text, over_textpos)
            self.screen.blit(coins_text, coins_textpos)
    

    def draw_gameover_screen(self, screen):
        screen.fill(config.BLACK)
        if pygame.font:
            over_text = pygame.font.Font(None, 36).render("GAME OVER !!!", 1, (255, 255, 255))
            quit_text = pygame.font.Font(None, 24).render("Press 'q' to get out of here.", 1, (255, 255, 255))
            over_textpos = over_text.get_rect(centerx=self.width/2, centery=self.height/2 - 36)
            quit_textpos = quit_text.get_rect(centerx=self.width/2, centery=self.height/2)
            self.screen.blit(over_text, over_textpos)
            self.screen.blit(quit_text, quit_textpos)


    def draw_dying_screen(self, screen):
        screen.fill((128, 128, 128, 128), None, pygame.BLEND_RGBA_MULT)
        if pygame.font:
            font = pygame.font.Font(None, 24)
            dead_text = font.render("You're dead.", 1, (255, 255, 255))
            again_text = font.render("Press ENTER to save the world one again !", 1, (255, 255, 255))
            dead_textpos = dead_text.get_rect(centerx=self.width/2, centery=self.height/2 - 36)
            again_textpos = again_text.get_rect(centerx=self.width/2, centery=self.height/2)
            self.screen.blit(dead_text, dead_textpos)
            self.screen.blit(again_text, again_textpos)


if __name__ == '__main__':
    g = MarioGame()
    g.init()
    g.run()
