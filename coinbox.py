import os
import pygame
import config
import coin
import powerup
import sprite_base

SECRET = 1
HIDDEN = 72
BLANK = 2

class CoinBox(sprite_base.SpriteBase):

    FRAME_WIDTH = 20
    COIN_WIDTH = 14
    FRAME_HEIGHT = 14
    PADDING = 0
    img_file = "map.png"
    count = 1
    my_coin = None
    ANIMATION_INTERVAL = 20
    FRAMES = [0, 1]

    def __init__(self, game, location, box_type, prize, count, *groups):
        self.box_type = box_type
        self.count = count
        self.prize = prize
        super(CoinBox, self).__init__(self.box_type, location, groups)
        if self.box_type == SECRET:
            self.set_blockers(game, "tlbr")

    def got_hit(self, game):
        my_pos = self.get_self_rect()
        if self.prize != None:
            powerup.PowerUp(self.rect.topleft, self.prize, game.powerups)
            self.prize = None
        else:
            if self.count:
                if self.my_coin == None:
                    config.play_sound(config.kaching_file)
                    if self.box_type == HIDDEN:
                        self.set_blockers(game, "tlbr")
                    location = (my_pos.midtop[0] - self.COIN_WIDTH/2, my_pos.top) 
                    self.my_coin = coin.Coin(location)
        if self.count:
            self.count -= 1
            game.my_mario.collected_coins += 1
        if self.box_type == HIDDEN or not self.count:
            self.box_type = BLANK


    def update_coin(self, dt, game):
        self.my_coin.update(dt, game)
        self.my_coin.rect.top -= dt * 200
        if self.my_coin.rect.top < self.rect.top - 130:
            self.my_coin.kill()
            self.my_coin = None

    def draw_coin(self, screen):
        if self.my_coin != None:
            self.my_coin.draw(screen)

    def update(self, dt, game):
        if self.box_type == SECRET:
            super(CoinBox, self).update(dt, game)
        else:
            self.set_sprite(self.box_type)
        if self.my_coin != None:
            self.update_coin(dt, game)
