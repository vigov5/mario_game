import sprite_base

class Turtle(sprite_base.SpriteBase):

    FRAME_WIDTH = 20
    FRAME_HEIGHT = 21
    PADDING = 1
    img_file = "red_turtle.png"
    RUNNING = [0, 1]
    SHELL_FRAMES = [0, 1, 2]
    FRAMES = None
    ANIMATION_INTERVAL = 10
    h_facing = "right"
    vx = 1
    state = "normal"
    h_state = "running"

    def __init__(self, location, *groups):
        self.FRAMES = self.RUNNING
        super(Turtle, self).__init__(0, location, *groups)


    def change_to_shell(self):
        self.state = "shell"
        self.h_state = "standing"
        self.vx = 0
        self.FRAME_HEIGHT = 13
        self.img_file = "red_turtle_shell.png"
        self.FRAMES = self.SHELL_FRAMES

    def do_shelling(self, mario):
        if mario.rect.centery < self.rect.centery:
            self.vx = -5
            self.h_facing = "right"
        else:
            self.h_facing = "left"
            self.vx = 5
        self.h_state = "running"

    def hit_platform_from_left(self, last, new, game):
        self.vx *= -1
        self.h_facing = "right"


    def hit_platform_from_right(self, last, new, game):
        self.vx *= -1
        self.h_facing = "left"


    def update(self, dt, game):
        last = self.rect.copy()
        self.apply_gravity()
        if self.state == "shell" and self.h_state == "standing":
            self.set_sprite(self.FRAMES[1])
        else:
            super(Turtle, self).update(dt, game)

        for brick in game.tilemap.layers["bricks"]:
            if brick.rect.colliderect(self.rect) \
                and self.rect.centery > brick.rect.top and self.rect.centery < brick.rect.bottom \
                and self.state == "shell" and self.h_state == "running":
                if not brick.broken:
                    brick.got_hit(game)
                    if self.h_facing == "left":
                        self.h_facing = "right"
                        self.vx = 5
                    elif self.h_facing == "right":
                        self.h_facing = "left"
                        self.vx = -5

        self.collision_with_platform(last, self.rect, game)
        self.hit_v_reversed_triggers(last, self.rect, game)
