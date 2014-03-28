import os
import pygame

image_path = "images"
sound_path = "sounds"
BLACK = 0, 0, 0
WHITE = 255, 255, 255
SKY = 95, 183, 229
BLANK_TILE = 72

kaching_file = "ka_ching.ogg"

# pool hold all sprites and images
images_pool = {}
sprites_pool = {}

def get_image_and_sprite(image_name):
    if image_name not in images_pool.keys():
        images_pool[image_name] = load_image(image_name)
        sprites_pool[image_name] = {}
    return images_pool[image_name], sprites_pool[image_name]


def load_image(image_name):
    _path = os.path.join(image_path, image_name)
    return pygame.image.load(_path)


def load_image_with_alpha(image_name):
    img = load_image(image_name)
    clip_rect = img.get_rect()
    _surface = pygame.Surface(clip_rect.size, pygame.SRCALPHA)
    _surface.blit(img, (0, 0), clip_rect)
    return _surface
