import pygame
from settings import *


class Div(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
	def create_rect(self,a,b,color):
		self.image = pygame.Surface((a,b))
		self.image.fill(color)
		self.rect = self.image.get_rect()


class Block(Div):
	def __init__(self, app, place):
		Div.__init__(self)
		self.app = app
		self.place = place
		self.size = 140
		self.margin = 7
		self.number = 0
		self.edited = False
		self.create_rect(self.size,self.size,NOTHING)
		self.rect.topleft = (app.WIDTH/2 + self.margin/2 + (self.size+self.margin)*(place[0]-2), app.HEIGHT/2+self.margin/2+(self.size+self.margin)*(place[1]-2))
	
	def new_color(self):
		color = (195,(self.number*7)%189+35,min(self.number%8*32+20, 255))
		if self.number == 0:
			color = NOTHING
		self.image.fill(color)