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

    def __init__(self, *groups):
        super(Mario, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.image = self.set_sprite(self.index)
        self.rect = self.image.get_rect()
        self.pos = self.rect
        self.vx = 0
        self.vy = 0
        self.v_state = "resting"
        self.h_state = "standing"
        self.facing = "right"
        self.state = "normal"

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.v_state == "resting":
                    self.jump()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_LEFT:
                self.move_left()
            elif event.key == pygame.K_DOWN:
                self.v_state = "crouching"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or \
                event.key == pygame.K_LEFT:
                self.vx = 0
                self.h_state = "standing"
            elif event.key == pygame.K_DOWN:
                self.v_state = "resting"

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

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

    def update(self, dt, game):
        last = self.rect.copy()
        if self.state == "pipeing":
            self.vy = 1
            self.vx = 0
        else:
            self.vx = min(self.MAX_VX, self.vx)
            self.vy = min(self.MAX_VY, self.vy)
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        self.rect = self.rect.move(dx, dy)

        new = self.rect
        if not self.state == "pipeing":
            # collison with pipe
            if self.v_state == "crouching":
                for pipe in game.tilemap.layers["triggers"].collide(new, "pipe"):
                    start_x = pipe.left + pipe.width/4
                    end_x = pipe.right - pipe.width/4
                    if last.bottom <= pipe.top and new.bottom > pipe.top \
                        and new.centerx > start_x and new.centerx < end_x:
                            # TODO do change scence and map
                            self.state = "pipeing"
                            self.pipe_y = pipe.top

            for box in game.tilemap.layers["coinboxs"]:
                # TODO check only box that inside current viewport
                if box.rect.colliderect(new) \
                    and new.centerx > box.rect.left and new.centerx < box.rect.right \
                    and last.top >= box.rect.bottom and new.top < box.rect.bottom:
                    box.got_hit(game)
                    new.top = box.rect.bottom
                    self.vy = 0
            for brick in game.tilemap.layers["bricks"]:
                # TODO check only brick that inside current viewport
                if brick.rect.colliderect(new) \
                    and new.centerx > brick.rect.left and new.centerx < brick.rect.right \
                    and last.top >= brick.rect.bottom and new.top < brick.rect.bottom:
                    if not brick.broken:
                        brick.got_hit(game)
                        new.top = brick.rect.bottom
                        self.vy = 0

            for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
                if last.bottom <= cell.top and new.bottom > cell.top \
                    and not (last.left == cell.right or last.right == cell.left):
                    new.bottom = cell.top
                    self.v_state = "resting"
                    self.vy = 0
                if last.top >= cell.bottom and new.top < cell.bottom \
                    and not (last.left == cell.right or last.right == cell.left):
                    new.top = cell.bottom
                    self.vy = 0
                if last.right <= cell.left and new.right > cell.left and last.bottom != cell.top:
                    new.right = cell.left
                if last.left >= cell.right and new.left < cell.right and last.bottom != cell.top:
                    new.left = cell.right
        else:
            if new.bottom >= self.pipe_y + new.height:
                self.state = "piped"
                self.pipe_y = None

        game.tilemap.set_focus(new.x, new.y)

        # change sprite
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            if self.v_state == "jumping":
                self.image = self.set_sprite(self.JUMP)
            else:
                if self.h_state == "running":
                    self.index = (self.index + 1) % len(self.RUNNING)
                    self.image = self.set_sprite(self.RUNNING[self.index])
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
