import sprite_base

class Turtle(sprite_base.SpriteBase):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 21
    PADDING = 1
    img_file = "red_turtle.png"
    RUNNING = [0, 1]
    FRAMES = None
    ANIMATION_INTERVAL = 10
    v_facing = "right"
    vx = 1

    def __init__(self, location, *groups):
        self.FRAMES = self.RUNNING
        super(Turtle, self).__init__(0, location, *groups)


    def hit_platform_from_left(self, last, new, game):
        self.vx *= -1
        self.v_facing = "right"


    def hit_platform_from_right(self, last, new, game):
        self.vx *= -1
        self.v_facing = "left"


    def update(self, dt, game):
        last = self.rect.copy()
        self.apply_gravity()
        self.collision_with_platform(last, self.rect, game)
        self.hit_v_reversed_triggers(last, self.rect, game)
        super(Turtle, self).update(dt, game)
