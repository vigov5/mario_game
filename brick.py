import os
import pygame
import config

class Brick(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 0
    TILE = [3, 4]
    img_file = "map.png"
    part_file = "part.png"
    GRAVITY = 0.2
    PART_SIZE = 5

    def __init__(self, game, location, *groups):
        super(Brick, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.image = self.set_sprite(self.TILE[0])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.group = groups
        self.set_blockers(game, "tlrb")
        self.broken = False
        self.particles_vx = [-2, -2, 2, 2]
        self.particles_vy = [-6, -2, -2, -6]
        self.particles = [None, None, None, None]

    def init_particles(self):
        my_pos = self.get_self_rect()
        location = (my_pos.centerx - self.PART_SIZE/2, my_pos.centery - self.PART_SIZE/2) 
        for i in range(len(self.particles)):
            self.particles[i] = pygame.sprite.Sprite()
            img_path = os.path.join(config.image_path, self.part_file)
            self.particles[i].image = pygame.image.load(img_path)
            self.particles[i].rect = self.particles[i].image.get_rect()
            self.particles[i].rect.x, self.particles[i].rect.y = location

    def get_self_rect(self):
        ox, oy = self.group[0].position
        sx, sy = self.rect.topleft
        return pygame.Rect(sx - ox, sy - oy, self.rect.width, self.rect.height)

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

    def update(self, dt, game):
        if self.broken:
            for i in range(len(self.particles)):
                if self.particles[i] != None:
                    self.particles_vy[i] += self.GRAVITY
                    self.particles_vy[i] = min(20, self.particles_vy[i] + self.GRAVITY)
                    self.particles[i].rect.x += self.particles_vx[i]
                    self.particles[i].rect.y += self.particles_vy[i]
                    if self.particles[i].rect.top > game.height:
                        self.particles[i].kill()
                        self.particles[i] = None
            if self.particles.count(None) == len(self.particles):
                self.kill()

    def draw_particles(self, screen):
        if self.broken:
            for p in self.particles:
                if p:
                    screen.blit(p.image, p.rect.topleft)

    def got_hit(self, game):
        self.set_blockers(game, None)
        if not self.broken:
            self.init_particles()
            self.broken = True
            self.image = self.set_sprite(config.BLANK_TILE)

    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]
