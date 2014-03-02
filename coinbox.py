import os
import pygame
import config

SECRET = 1
HIDE = 72
BLANK = 2

class CoinBox(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 0
    img_file = "map.png"
    count = 1

    def __init__(self, location, box_type, *groups):
        super(CoinBox, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.box_type = box_type
        self.image = self.set_sprite(self.box_type)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

    def got_hit(self):
        if self.count:
            self.count -= 1
        else:
            self.box_type = BLANK

    def update(self, dt, game):
        self.image = self.set_sprite(self.box_type)
        
    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]