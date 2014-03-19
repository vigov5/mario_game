import os
import pygame
import config

MUSHROOM = 0
BAD_FUNGUS = 1
ONE_UP = 2
FLOWER = 3

class PowerUp(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 1
    img_file = "powerup.png"

    GRAVITY = 0.4
    MAX_VX = 3
    MAX_VY = 20

    def __init__(self, location, power_type, *groups):
        super(PowerUp, self).__init__(groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.type = power_type
        self.image = self.set_sprite(self.type)
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.start_y = location[1]
        self.vx = 0
        self.vy = -4
        self.state = "creating"

    def update(self, dt, game):
        last = self.rect.copy()
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        self.rect = self.rect.move(dx, dy)

        if self.state == "creating":
            if self.rect.y < self.start_y - 14:
                self.state = "drifting"
        else:
            for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
                self.vx *= -1
                break

            new = self.rect
            for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
                if last.bottom <= cell.top and new.bottom > cell.top \
                    and not (last.left == cell.right or last.right == cell.left):
                    new.bottom = cell.top
                    self.vy = 0
                    if self.vx == 0 and self.type != FLOWER:
                        self.vx = 1
                if last.top >= cell.bottom and new.top < cell.bottom \
                        and not (last.left == cell.right or last.right == cell.left):
                    new.top = cell.bottom
                    self.vy = 0
                if last.right <= cell.left and new.right > cell.left and last.bottom != cell.top:
                    new.right = cell.left
                    self.vx *= -1
                if last.left >= cell.right and new.left < cell.right and last.bottom != cell.top:
                    new.left = cell.right
                    self.vx *= -1

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