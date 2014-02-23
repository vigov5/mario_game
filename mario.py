import os
import pygame

import config

class Mario(pygame.sprite.Sprite):

	FRAME_WIDTH = 20
	FRAME_HEIGHT = 19
	PADDING = 1
	img_file = "small_mario.png"
	STAND = 0
	RUNNING = [0, 1]
	index = STAND
	loaded_sprites = {}
	ANIMATION_INTERVAL = 10

	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		img_path = os.path.join(config.image_path, self.img_file)
		self.sprite_imgs = pygame.image.load(img_path)
		self.image = self.set_sprite(self.index)
		self.rect = self.image.get_rect()
		self.pos = self.rect
		self.game = game

	def handle(self, event):
		pass

	def update(self):
		# change sprite
		if self.game.time_step % self.ANIMATION_INTERVAL == 0:
			self.index = (self.index + 1) % len(self.RUNNING)
			self.image = self.set_sprite(self.index)

	def set_sprite(self, index):
		if index not in self.loaded_sprites.keys():
			left = (self.FRAME_WIDTH + self.PADDING) * index
			rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
			_surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
			_surface.blit(self.sprite_imgs, (0, 0), rect)
			self.loaded_sprites[index] = _surface

		return self.loaded_sprites[index]
