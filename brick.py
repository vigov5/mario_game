import os
import pygame
import sprite_base
import config

class Brick(sprite_base.SpriteBase):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 0
    TILE = [3, 4]
    img_file = "map.png"
    part_file = "part.png"
    PART_GRAVITY = 0.2
    GRAVITY = 0
    PART_SIZE = 5

    def __init__(self, game, location, *groups):
        super(Brick, self).__init__(self.TILE[0], location, groups)
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


    def update(self, dt, game):
        last = self.rect.copy()
        if self.broken:
            for i in range(len(self.particles)):
                if self.particles[i] != None:
                    self.particles_vy[i] += self.PART_GRAVITY
                    self.particles_vy[i] = min(20, self.particles_vy[i] + self.PART_GRAVITY)
                    self.particles[i].rect.x += self.particles_vx[i]
                    self.particles[i].rect.y += self.particles_vy[i]
                    if self.particles[i].rect.top > game.height:
                        self.particles[i].kill()
                        self.particles[i] = None
            if self.particles.count(None) == len(self.particles):
                self.kill()
        if self.state == "throwed" and not self.broken:
            self.apply_gravity()
            new = self.rect
            for hit_brick in game.tilemap.layers["bricks"]:
                # TODO check only hit_brick that inside current viewport
                if hit_brick.rect.colliderect(new) and hit_brick != self:
                    self.got_hit(game)
                    hit_brick.got_hit(game)
                    break
            if not self.broken:
                self.collision_with_platform(last, new, game)

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
            self.set_sprite(config.BLANK_TILE)

    def hit_platform_from_left(self, last, new, game):
        self.got_hit(game)

    def hit_platform_from_right(self, last, new, game):
        self.got_hit(game)