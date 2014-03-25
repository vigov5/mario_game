import pygame
import powerup

import sprite_base

class Mario(sprite_base.SpriteBase):

    PADDING = 1
    sprite_imgs = {
        "small": "small_mario.png",
        "medium" : "medium_mario.png"
    }
    cell_sizes = {
        "small": [(20, 19), (20, 19), (20, 19), (20, 19)],
        "medium": [(19, 26), (19, 26), (20, 26), (20, 27)],
    }

    STAND = 0
    RUNNING = [0, 1]
    JUMP = 3
    ANIMATION_INTERVAL = 5
    frames_sizes = None

    state = "normal"
    pipe_obj = None
    grow_size = "small"

    def __init__(self, location, *groups):
        self.grow_up("small")
        self.FRAMES = self.RUNNING
        self.frame_index = self.FRAMES[0]
        self.frames_sizes = self.cell_sizes[self.grow_size]
        super(Mario, self).__init__(self.STAND, location, groups)


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


    def jump(self):
        self.vy = -9
        self.v_state = "jumping"


    def move_left(self):
        self.vx = -2.5
        self.h_state = "running"
        self.v_facing = "left"


    def move_right(self):
        self.vx = 2.5
        self.h_state = "running"
        self.v_facing = "right"


    def grow_up(self, size):
        self.grow_size = size
        self.img_file = self.sprite_imgs[self.grow_size]


    def update(self, dt, game):
        last = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.x = last.x
        self.rect.y = last.y
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
                            self.pipe_obj = pipe
                            break
            # collison with power up
            for p in game.tilemap.layers["powerups"]:
                if p.rect.colliderect(new) and p.state != "creating":
                    if p.type == powerup.MUSHROOM:
                        self.grow_up("medium")
                    p.kill()
                    break

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
                        if self.grow_size != "small":
                            brick.got_hit(game)
                        new.top = brick.rect.bottom
                        self.vy = 0

            self.collision_with_platform(last, new, game)
        else:
            if new.bottom >= self.pipe_y + new.height:
                self.state = "piped"
                self.pipe_y = None

        game.tilemap.set_focus(new.x, new.y)

        # change sprite
        self.frames_sizes = self.cell_sizes[self.grow_size]
        if self.v_state == "jumping":
            self.set_sprite(self.JUMP)
        else:
            if self.h_state == "standing":
                self.set_sprite(self.STAND)
            elif self.h_state == "running":
                super(Mario, self).update(dt, game)


    def hit_platform_from_bottom(self, last, new, game):
        self.v_state = "resting"
