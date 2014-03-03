import os
import math
import pygame

import config

class Turtle(pygame.sprite.Sprite):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 21
    PADDING = 1
    img_file = "red_turtle.png"
    RUNNING = [0, 1]
    index = RUNNING[0]
    loaded_sprites = {}
    ANIMATION_INTERVAL = 10

    GRAVITY = 0.4
    MAX_VX = 3
    MAX_VY = 20

    def __init__(self, location, *groups):
        super(Turtle, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.image = self.set_sprite(self.index)
        self.rect = self.image.get_rect()
        self.pos = self.rect
        self.vx = 0
        self.vy = 0
        self.v_state = "resting"
        self.h_state = "running"
        self.facing = "right"
        self.set_position(location[0], location[1])

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, dt, game):
        last = self.rect.copy()
        if self.facing == "right":
            self.vx = 1
        elif self.facing == "left":
            self.vx = -1
        """
        if abs(self.vx) > self.MAX_VX:
            self.vx = math.copysign(self.MAX_VX, self.vx)
        if abs(self.vy) > self.MAX_VY:
            self.vy = math.copysign(self.MAX_VY, self.vy)
        """
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        self.rect = self.rect.move(dx, dy)

        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            if self.facing == "right":
                self.facing = "left"
            elif self.facing == "left":
                self.facing = "right"

        new = self.rect
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
                self.facing = "left"
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
                self.facing = "right"
            if last.bottom <= cell.top and new.bottom > cell.top:
                new.bottom = cell.top
                self.vy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.vy = 0

        # change sprite
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            self.index = (self.index + 1) % len(self.RUNNING)
            self.image = self.set_sprite(self.index)

            if self.facing == "left":
                self.image = pygame.transform.flip(self.image, True, False)

    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]

