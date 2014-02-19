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

	def __init__(self):
		img_path = os.path.join(config.image_path, self.img_file)
		self.all_sprite = pygame.image.load(img_path)
		self.image = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
		self.set_sprite(self.index)
		self.rect = self.image.get_rect()
		self.pos = self.rect
		print self.pos

	def handle(self, event):
		pass

	def update(self):
		self.index = (self.index + 1) % len(self.RUNNING)
		self.set_sprite(self.index)
		self.pos.x += 1
		print self.index

	def draw(self, screen):
		screen.blit(self.image, self.pos)


	def set_sprite(self, index):
		left = (self.FRAME_WIDTH + self.PADDING) * index
		rect = pygame.Rect(left, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
		self.image.blit(self.all_sprite, (0, 0), rect)
