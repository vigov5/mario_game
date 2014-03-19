import os
import pygame
import config
import coin
import powerup

SECRET = 1
HIDDEN = 72
BLANK = 2

class CoinBox(pygame.sprite.Sprite):

    loaded_sprites = {}
    FRAME_WIDTH = 20
    COIN_WIDTH = 14
    FRAME_HEIGHT = 14
    PADDING = 0
    img_file = "map.png"
    kaching_file = "ka_ching.mp3"
    count = 1
    my_coin = None
    index = 0
    ANIMATION_INTERVAL = 20

    def __init__(self, game, location, box_type, prize, count, *groups):
        super(CoinBox, self).__init__(*groups)
        img_path = os.path.join(config.image_path, self.img_file)
        self.sprite_imgs = pygame.image.load(img_path)
        self.box_type = box_type
        self.count = count
        self.image = self.set_sprite(self.box_type)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.group = groups
        self.prize = prize
        if self.box_type == SECRET:
            self.set_blockers(game, "tlbr")

    def set_blockers(self, game, value):
        cells = game.tilemap.layers['triggers'].get_in_region(
            self.rect.centerx, self.rect.centery, self.rect.centerx, self.rect.centery
        )
        for cell in cells:
            if getattr(cell, "tile"):
                if value:
                    cell.properties["blockers"] = value
                else:
                    del cell.properties["blockers"]

    def got_hit(self, game):
        my_pos = self.get_self_rect()
        if self.prize != None:
            powerup.PowerUp(self.rect.topleft, self.prize, game.powerups)
            self.prize = None
        else:
            if self.count:
                if self.my_coin == None:
                    pygame.mixer.music.load(os.path.join(config.sound_path, self.kaching_file))
                    pygame.mixer.music.play()
                    if self.box_type == HIDDEN:
                        self.set_blockers(game, "tlbr")
                    location = (my_pos.midtop[0] - self.COIN_WIDTH/2, my_pos.top) 
                    self.my_coin = coin.Coin(location)
        if self.count: self.count -= 1
        if self.box_type == HIDDEN or not self.count:
            self.box_type = BLANK

    def get_self_rect(self):
        ox, oy = self.group[0].position
        sx, sy = self.rect.topleft
        return pygame.Rect(sx - ox, sy - oy, self.rect.width, self.rect.height)

    def update_coin(self, dt, game):
        self.my_coin.update(dt, game)
        self.my_coin.rect.y -= dt * 200
        if self.my_coin.rect.y < self.rect.y - 130:
            self.my_coin.kill()
            self.my_coin = None

    def draw_coin(self, screen):
        if self.my_coin != None:
            self.my_coin.draw(screen)

    def update(self, dt, game):
        frames = [0, 1]
        if game.time_step % self.ANIMATION_INTERVAL == 0:
            if self.box_type == SECRET:
                self.index = (self.index + 1) % 2
                self.image = self.set_sprite(frames[self.index])
            else:
                self.image = self.set_sprite(self.box_type)
        if self.my_coin != None:
            self.update_coin(dt, game)
        
    def set_sprite(self, index):
        if index not in self.loaded_sprites.keys():
            left = (self.FRAME_WIDTH + self.PADDING) * index
            rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
            _surface.blit(self.sprite_imgs, (0, 0), rect)
            self.loaded_sprites[index] = _surface

        return self.loaded_sprites[index]