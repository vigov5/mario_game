import os
import pygame
import config

RED_FLOWER = 0
GREEN_FLOWER = 2

class Flower(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 24
    FRAME_HEIGHT = 17
    PADDING = 1
    img_file = "flower.png"
    ANIMATION_INTERVAL = 20

    def __init__(self, game, location, color, *groups):
        super(Flower, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.index = color
        self.color = color
        self.image = self.set_sprite(self.index)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.rect.x += (40 - self.rect.width)/2
        self.rect.y -= 3
        self.group = groups

    def get_self_rect(self):
        ox, oy = self.group[0].position
        sx, sy = self.rect.topleft
        return pygame.Rect(sx - ox, sy - oy, self.rect.width, self.rect.height)

    def update(self, dt, game):
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            self.index = (self.index + 1) % 2
            if self.color == GREEN_FLOWER:
                self.index += 2
            self.image = self.set_sprite(self.index)

    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]
