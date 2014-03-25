import sprite_base

RED_FLOWER = 0
GREEN_FLOWER = 2

class Flower(sprite_base.SpriteBase):

    loaded_sprites = {}
    FRAME_WIDTH = 24
    FRAME_HEIGHT = 17
    PADDING = 1
    img_file = "flower.png"
    ANIMATION_INTERVAL = 40
    h_facing = "down"

    def __init__(self, game, location, color, *groups):
        self.color = color
        if self.color == GREEN_FLOWER:
            self.FRAMES = [2, 3]
        else:
            self.FRAMES = [0, 1]
        super(Flower, self).__init__(self.frame_index, location, groups)
        self.rect.left += (40 - self.rect.width)/2
        self.rect.top -= 3
        self.pivot_y = self.rect.top

    def update(self, dt, game):
        if game.time_step % 4 == 0:
            if self.h_facing == "down":
                self.rect.top += 1
            elif self.h_facing == "up":
                self.rect.top -= 1

        if self.rect.top >= self.pivot_y + self.rect.height and self.h_facing == "down":
            self.rect.top = self.pivot_y + self.rect.height
            self.h_facing = "up"
        elif self.h_facing == "up" and self.rect.top <= self.pivot_y:
            self.rect.top = self.pivot_y
            if game.time_step % 240 == 0:
                self.h_facing = "down"

        super(Flower, self).update(dt, game)
