import os
import pygame
import config

SECRET = 1
HIDE = 72
BLANK = 2

class Coin(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 14
    FRAME_HEIGHT = 13
    PADDING = 1
    img_file = "coin.png"
    count = 1
    FRAMES = [0, 1, 2, 1]
    index = FRAMES[0]
    ANIMATION_INTERVAL = 20

    def __init__(self, location):
        super(Coin, self).__init__()
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.image = self.set_sprite(self.index)
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def update(self, dt, game):
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            self.index = (self.index + 1) % len(self.FRAMES)
            self.image = self.set_sprite(self.FRAMES[self.index])

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]