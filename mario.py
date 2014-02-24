import os
import math
import pygame

import config

class Mario(pygame.sprite.Sprite):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 19
    PADDING = 1
    img_file = "small_mario.png"
    STAND = 0
    RUNNING = [0, 1]
    JUMP = 3
    index = STAND
    loaded_sprites = {}
    ANIMATION_INTERVAL = 5

    GRAVITY = 0.4
    MAX_VX = 3
    MAX_VY = 20

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.image = self.set_sprite(self.index)
        self.rect = self.image.get_rect()
        self.pos = self.rect
        self.game = game
        self.vx = 0
        self.vy = 0
        self.v_state = "standing"
        self.h_state = "standing"
        self.facing = "right"

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.v_state == "standing":
                    self.jump()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_LEFT:
                self.move_left()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or \
                event.key == pygame.K_LEFT:
                self.vx = 0
                self.h_state = "standing"

    def jump(self):
        self.vy = -9
        self.v_state = "jumping"

    def move_left(self):
        self.vx = -2.5
        self.h_state = "running"
        self.facing = "left"

    def move_right(self):
        self.vx = 2.5
        self.h_state = "running"
        self.facing = "right"


    def update(self):
        if abs(self.vx) > self.MAX_VX:
            self.vx = math.copysign(self.MAX_VX, self.vx)
        if abs(self.vy) > self.MAX_VY:
            self.vy = math.copysign(self.MAX_VY, self.vy)
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        self.rect = self.rect.move(dx, dy)
        if self.rect.bottom > 200:
            self.rect.bottom = 200
            self.v_state = "standing"
            self.vy = 0

        # change sprite
        if self.game.time_step % self.ANIMATION_INTERVAL == 0:
            if self.v_state == "jumping":
                self.image = self.set_sprite(self.JUMP)
            else:
                if self.h_state == "running":
                    self.index = (self.index + 1) % len(self.RUNNING)
                    self.image = self.set_sprite(self.index)
                elif self.h_state == "standing":
                    self.image = self.set_sprite(self.STAND)

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
