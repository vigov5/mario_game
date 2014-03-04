import os
import pygame
import config
import coin

SECRET = 1
HIDE = 72
BLANK = 2

class CoinBox(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 0
    img_file = "map.png"
    count = 10
    my_coin = None

    def __init__(self, location, box_type, *groups):
        super(CoinBox, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.box_type = box_type
        self.image = self.set_sprite(self.box_type)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.group = groups
        print self.rect

    def got_hit(self):
        if self.count:
            if self.my_coin == None:
                my_pos = self.get_self_rect()
                location = (my_pos.midtop[0] - 7, my_pos.top) 
                self.my_coin = coin.Coin(location)
                self.count -= 1

        if not self.count:
            self.box_type = BLANK

    def get_self_rect(self):
        ox, oy = self.group[0].position
        sx, sy = self.rect.topleft
        return pygame.Rect(sx - ox, sy - oy, self.rect.width, self.rect.height)

    def update_coin(self, dt, game):
        self.my_coin.update(dt, game)
        self.my_coin.rect.y -= dt * 200
        if self.my_coin.rect.y < self.rect.y - 130:
            self.my_coin.kill()
            self.my_coin = None

    def draw_coin(self, screen):
        if self.my_coin != None:
            self.my_coin.draw(screen)

    def update(self, dt, game):
        self.image = self.set_sprite(self.box_type)
        if self.my_coin != None:
            self.update_coin(dt, game)
        
    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]