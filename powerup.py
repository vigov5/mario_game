import sprite_base

MUSHROOM = 0
BAD_FUNGUS = 1
ONE_UP = 2
FLOWER = 3

class PowerUp(sprite_base.SpriteBase):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 14
    PADDING = 1
    img_file = "powerup.png"

    def __init__(self, location, power_type, *groups):
        self.type = power_type
        self.start_y = location[1]
        self.vx = 0
        self.vy = -4
        self.state = "creating"
        super(PowerUp, self).__init__(self.type, location, groups)

    def hit_platform_from_bottom(self, last, new, game):
        if self.vx == 0 and self.type != FLOWER:
            self.vx = 1

    def hit_platform_from_right(self, last, new, game):
        self.vx *= -1

    def hit_platform_from_left(self, last, new, game):
        self.vx *= -1

    def update(self, dt, game):
        last = self.rect.copy()
        self.apply_gravity()

        if self.state == "creating":
            if self.rect.top < self.start_y - 14:
                self.state = "drifting"
        else:
            self.hit_v_reversed_triggers(last, self.rect, game)
            self.collision_with_platform(last, self.rect, game)
