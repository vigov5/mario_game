import pygame
import powerup
import turtle
import flower
import config
import sprite_base

class Mario(sprite_base.SpriteBase):

    PADDING = 1
    sprite_imgs = {
        "small": "small_mario.png",
        "medium" : "medium_mario.png"
    }
    cell_sizes = {
        "small": [(20, 19), (20, 19), (20, 19), (20, 19)],
        "medium": [(19, 26), (19, 26), (20, 26), (20, 27)],
    }

    STAND = 0
    RUNNING = [0, 1]
    JUMP = 3
    ANIMATION_INTERVAL = 5
    frames_sizes = None

    state = "normal"
    pipe_obj = None
    grow_size = "small"
    invi_time = 60
    halo = None
    lives = 3
    collected_coins = 0
    my_brick = None

    def __init__(self, location, *groups):
        self.grow_up("small")
        self.FRAMES = self.RUNNING
        self.frame_index = self.FRAMES[0]
        self.frames_sizes = self.cell_sizes[self.grow_size]
        super(Mario, self).__init__(self.STAND, location, groups)


    def handle(self, event):
        if self.state != "dying":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.v_state == "resting":
                        self.jump()
                elif event.key == pygame.K_RIGHT:
                    self.move_right()
                elif event.key == pygame.K_LEFT:
                    self.move_left()
                elif event.key == pygame.K_DOWN:
                    self.v_state = "crouching"
                elif event.key == pygame.K_SPACE:
                    if self.my_brick:
                        self.my_brick.state = "throwed"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_LEFT:
                    self.vx = 0
                    self.h_state = "standing"
                elif event.key == pygame.K_DOWN:
                    self.v_state = "resting"
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    self.state = "reborn"


    def jump(self, speed=9):
        self.vy = -1*speed
        self.v_state = "jumping"


    def move_left(self):
        self.vx = -2.5
        self.h_state = "running"
        self.h_facing = "left"


    def move_right(self):
        self.vx = 2.5
        self.h_state = "running"
        self.h_facing = "right"


    def grow_up(self, size):
        self.grow_size = size
        self.img_file = self.sprite_imgs[self.grow_size]
        if size == "medium":
            self.rect.top -= 10

    def update(self, dt, game):
        last = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.x = last.x
        self.rect.y = last.y
        if self.state == "pipeing":
            self.vy = 1
            self.vx = 0
        elif self.state == "dying":
            self.vy = -1
            self.vx = 0
        else:
            self.vx = min(self.MAX_VX, self.vx)
            self.vy = min(self.MAX_VY, self.vy)
        dy = self.vy
        dx = self.vx
        self.vy += self.GRAVITY
        self.rect = self.rect.move(dx, dy)

        new = self.rect
        if self.state == "reborn":
            self.reborn(game)
        elif self.state == "dying":
            self.halo.rect.top = self.rect.top - 10
        elif not self.state == "pipeing":
            # collison with pipe
            if self.v_state == "crouching":
                for pipe in game.tilemap.layers["triggers"].collide(new, "pipe"):
                    start_x = pipe.left + pipe.width/4
                    end_x = pipe.right - pipe.width/4
                    if last.bottom <= pipe.top and new.bottom > pipe.top \
                        and new.centerx > start_x and new.centerx < end_x:
                            # TODO do change scence and map
                            self.state = "pipeing"
                            self.pipe_y = pipe.top
                            self.pipe_obj = pipe
                            break
            # collison with power up
            for p in game.tilemap.layers["powerups"]:
                if p.rect.colliderect(new) and p.state != "creating":
                    if p.type == powerup.MUSHROOM:
                        self.grow_up("medium")
                    elif p.type == powerup.ONE_UP:
                        self.lives += 1
                        config.play_sound(config.one_up_file)
                    p.kill()
                    break

            for box in game.tilemap.layers["coinboxs"]:
                # TODO check only box that inside current viewport
                if box.rect.colliderect(new) \
                    and new.centerx > box.rect.left and new.centerx < box.rect.right \
                    and last.top >= box.rect.bottom and new.top < box.rect.bottom:
                    box.got_hit(game)
                    new.top = box.rect.bottom
                    self.vy = 0
            for brick in game.tilemap.layers["bricks"]:
                # TODO check only brick that inside current viewport
                if brick.rect.colliderect(new) \
                    and new.centerx > brick.rect.left and new.centerx < brick.rect.right \
                    and last.top >= brick.rect.bottom and new.top < brick.rect.bottom \
                    and brick != self.my_brick:
                    if not brick.broken:
                        new.top = brick.rect.bottom
                        self.vy = 0
                        if self.grow_size != "small":
                            brick.got_hit(game)
                        elif self.grow_size == "small" and not self.my_brick \
                            and pygame.key.get_pressed()[pygame.K_SPACE]:
                            self.my_brick = brick
                            self.my_brick.state = "holded"
                            brick.set_blockers(game, None)
            for enemy in game.tilemap.layers["enemies"]:
                # TODO check only enemy that near mario
                if enemy.rect.colliderect(new):
                    if isinstance(enemy, turtle.Turtle):
                        self.hit_turtle(last, new, enemy, game)
                    elif isinstance(enemy, flower.Flower):
                        self.got_damaged(game)

            for coin in game.tilemap.layers["coins"]:
                if coin.rect.colliderect(new):
                    coin.kill()
                    self.collected_coins += 1
                    config.play_sound(config.kaching_file)

            self.collision_with_platform(last, new, game)

            if self.my_brick:
                if self.h_facing == "left":
                    if self.my_brick.state == "holded":
                        self.my_brick.rect.top = self.rect.top
                        self.my_brick.rect.left = self.rect.left - 14
                    elif self.my_brick.state == "throwed":
                        self.my_brick.turn_with_speed("left", -10)
                        self.my_brick = None
                else:
                    if self.my_brick.state == "holded":
                        self.my_brick.rect.top = self.rect.top
                        self.my_brick.rect.right = self.rect.right + 14
                    elif self.my_brick.state == "throwed":
                        self.my_brick.turn_with_speed("right", 10)
                        self.my_brick = None

            # quick hack
            if self.rect.top - 80 > game.height:
               self.go_dying(game)
        else:
            if new.bottom >= self.pipe_y + new.height:
                self.state = "piped"
                self.pipe_y = None

        game.tilemap.set_focus(new.x, new.y)

        # change sprite
        self.frames_sizes = self.cell_sizes[self.grow_size]
        if self.state == "invicible":
            self.invi_time -= 1
            if self.invi_time == 0:
                self.back_to_normal()
        if self.v_state == "jumping":
            self.set_sprite(self.JUMP)
        else:
            if self.h_state == "standing":
                self.set_sprite(self.STAND)
            elif self.h_state == "running":
                super(Mario, self).update(dt, game)


    def go_dying(self, game):
        self.state = "dying"
        self.create_halo_ring(game)
        self.vx, self.vy = (0, -1)
        self.v_state = "jumping"
        self.GRAVITY = 0
        self.lives -= 1
        if self.my_brick:
            self.my_brick.got_hit(game)
            self.my_brick = None
        if self.lives == 0:
            game.game_over = True


    def reborn(self, game):
        start_cell = game.tilemap.layers['triggers'].find('player')[0]
        self.rect.topleft = (start_cell.px, start_cell.py)
        self.state = "normal"
        self.v_state = "resting"
        self.h_state = "standing"
        self.became_invicible()
        self.vx, self.vy = (0, 0)
        self.GRAVITY = 0.4
        game.sprites.remove(self.halo)

    def became_invicible(self):
        self.state = "invicible"
        self.opacity = 128
        self.invi_time = 60

    def back_to_normal(self):
        self.state = "normal"
        self.opacity = 255
        self.invi_time = 60


    def create_halo_ring(self, game):
        if not self.halo:
            self.halo = pygame.sprite.Sprite()
            self.halo.image = config.load_image_with_alpha("halo.png")
            self.halo.rect = self.halo.image.get_rect()
        self.halo.rect.topleft = self.rect.topleft
        self.halo.rect.top = self.rect.top - 10
        self.halo.rect.left += (self.rect.width - self.halo.rect.width)/2
        game.sprites.add(self.halo)


    def hit_platform_from_bottom(self, last, new, game):
        self.v_state = "resting"


    def hit_turtle(self, last, new, enemy, game):
        if last.bottom <= enemy.rect.top and new.bottom >= enemy.rect.top:
            self.jump(12)
            if enemy.state == "normal":
                enemy.change_to_shell()
            elif enemy.state == "shell":
                if enemy.h_state == "running":
                    enemy.change_to_shell()
                else:
                    enemy.do_shelling(self)
        elif enemy.state == "shell" and enemy.h_state == "standing":
            enemy.h_state = "running"
            if self.rect.left < enemy.rect.left:
                enemy.turn_with_speed("right", 5)
            else:
                enemy.turn_with_speed("left", -5)
        else:
            self.got_damaged(game)


    def got_damaged(self, game):
        if self.grow_size == "medium":
            self.grow_up("small")
            self.became_invicible()
        elif self.state != "invicible":
            self.go_dying(game)             
