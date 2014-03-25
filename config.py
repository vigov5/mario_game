import os
import pygame

image_path = "images"
sound_path = "sounds"
BLACK = 0, 0, 0
WHITE = 255, 255, 255
SKY = 95, 183, 229
BLANK_TILE = 72

# pool hold all sprites and images
images_pool = {}
sprites_pool = {}

def get_image_and_sprite(image_name):
    if image_name not in images_pool.keys():
        _path = os.path.join(image_path, image_name)
        images_pool[image_name] = pygame.image.load(_path)
        sprites_pool[image_name] = {}
    return images_pool[image_name], sprites_pool[image_name]
