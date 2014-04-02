import pygame
import config

SECRET = 1
HIDE = 72
BLANK = 2

class SpriteBase(pygame.sprite.Sprite):

    FRAME_WIDTH = 0
    FRAME_HEIGHT = 0
    PADDING = 1
    img_file = ""
    opacity = 255

    GRAVITY = 0.4
    MAX_VX = 3
    MAX_VY = 20

    vx = 0
    vy = 0
    # vertical and horizontal state
    h_state = "standing"
    v_state = "resting"
    # vertical and horizontal facing
    v_facing = "up"
    h_facing = "right"
    # general state
    state = ""

    frames_sizes = None
    FRAMES = []

    frame_index = 0
    rect = None
    dead = False

    def init_image_and_position(self, index, location):
        self.set_sprite(index)
        self.rect = self.image.get_rect()
        self.rect.topleft = location


    def __init__(self, index, location, *groups):
        if groups:
            self.group = groups[0]
            super(SpriteBase, self).__init__(*groups)
        else:
            super(SpriteBase, self).__init__()
        self.init_image_and_position(index, location)


    def update(self, dt, game):
        """loop through all frames and change sprite"""
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            self.frame_index = (self.frame_index + 1) % len(self.FRAMES)
            self.set_sprite(self.FRAMES[self.frame_index])


    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


    def get_clip_rect(self, index):
        left = 0
        if self.frames_sizes == None:
            left = (self.FRAME_WIDTH + self.PADDING) * index
            width, height = self.FRAME_WIDTH, self.FRAME_HEIGHT
        else:
            for i in range(index):
                left += self.frames_sizes[i][0] + self.PADDING
            width, height = self.frames_sizes[index]
        return pygame.Rect(left, 0, width, height)


    def set_sprite(self, index):
        self.image = None
        img, cached = config.get_image_and_sprite(self.img_file)
        key_name = "_".join(map(str, [index, self.opacity]))
        if key_name not in cached.keys():
            clip_rect = self.get_clip_rect(index)
            _surface = pygame.Surface(clip_rect.size, pygame.SRCALPHA)
            _surface.blit(img, (0, 0), clip_rect)
            # this works on images with per pixel alpha too
            _surface.fill((255, 255, 255, self.opacity), None, pygame.BLEND_RGBA_MULT)
            cached[key_name] = _surface

        self.image = cached[key_name]
        if self.rect and self.rect.size != self.image.get_rect().size:
            self.rect.size = self.image.get_rect().size
        # flip image if needed
        if self.h_facing == "left":
            self.image = pygame.transform.flip(self.image, True, False)


    def hit_platform_from_top(self, last, new, game):
        pass


    def hit_platform_from_bottom(self, last, new, game):
        pass


    def hit_platform_from_left(self, last, new, game):
        pass


    def hit_platform_from_right(self, last, new, game):
        pass


    def apply_gravity(self):
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        self.rect = self.rect.move(dx, dy)


    def collision_with_platform(self, last, new, game):
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            if last.bottom <= cell.top and new.bottom > cell.top \
                and not (last.left == cell.right or last.right == cell.left):
                new.bottom = cell.top
                self.vy = 0
                self.hit_platform_from_bottom(last, new, game)
            if last.top >= cell.bottom and new.top < cell.bottom \
                    and not (last.left == cell.right or last.right == cell.left):
                new.top = cell.bottom
                self.vy = 0
                self.hit_platform_from_top(last, new, game)
            if last.right <= cell.left and new.right > cell.left and last.bottom != cell.top:
                new.right = cell.left
                self.hit_platform_from_right(last, new, game)
            if last.left >= cell.right and new.left < cell.right and last.bottom != cell.top:
                new.left = cell.right
                self.hit_platform_from_left(last, new, game)


    def turn_with_speed(self, direction, speed):
        self.h_facing = direction
        self.vx = speed


    def hit_v_reversed_triggers(self, last, new, game):
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'v_reverse'):
            if self.h_facing == "left":
                self.turn_with_speed("right", 1)
            elif self.h_facing == "right":
                self.turn_with_speed("left", -1)
            break


    def set_blockers(self, game, value):
        cells = game.tilemap.layers['triggers'].get_in_region(
            self.rect.centerx, self.rect.centery, self.rect.centerx, self.rect.centery
        )
        for cell in cells:
            if getattr(cell, "tile"):
                if value:
                    cell.properties["blockers"] = value
                elif cell.properties.get("blockers"):
                    del cell.properties["blockers"]
            break

    def get_self_rect(self):
        ox, oy = self.group[0].position
        sx, sy = self.rect.topleft
        return pygame.Rect(sx - ox, sy - oy, self.rect.width, self.rect.height)
