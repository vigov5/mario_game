import sprite_base

class Coin(sprite_base.SpriteBase):

    FRAME_WIDTH = 14
    FRAME_HEIGHT = 13
    img_file = "coin.png"
    FRAMES = [0, 1, 2, 1]
    ANIMATION_INTERVAL = 20

    def __init__(self, location, *groups):
        super(Coin, self).__init__(0, location, groups)
