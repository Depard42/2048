import pygame
import pygame.freetype
import random
from settings import *
from div import *


class Game:
	def __init__(self, app):
		self.app = app
		self.font = pygame.freetype.SysFont('Comic Sans MS', 36)
		self.score = 0
		# create background
		self.back = Div()
		self.app.all_sprites.add(self.back)
		self.back.create_rect(self.app.WIDTH-40, app.HEIGHT-700, MAINCOLOR)
		self.back.rect.center =(self.app.WIDTH/2, self.app.HEIGHT/2)
		#create topic for score
		self.topic = Div()
		self.app.all_sprites.add(self.topic)
		self.topic.create_rect(400, 70, MAINCOLOR)
		self.topic.rect.center =(self.app.WIDTH/2, 100)
		#records
		self.rec = Div()
		self.app.all_sprites.add(self.rec)
		self.rec.create_rect(400, 70, MAINCOLOR)
		self.rec.rect.center =(self.app.WIDTH/2, self.app.HEIGHT -210)
		try:
			with open("record.txt", 'r') as file:
				self.record = int(file.read())
		except:
			self.record = 0
		#create blocks
		self.block_list = []
		self.block_map = []
		self.block_blank = []
		for i in range(4):
			self.block_map.append([])
			for j in range (4):
				block = Block(app, (i,j))
				self.block_map[i].append(block)
				self.block_list.append(block)
				self.block_blank.append(block)
				self.app.all_sprites.add(block)
	
	def generate_new(self):
		try:
			index = random.randrange(len(self.block_blank))
			num = self.block_blank[index].number = random.randrange(2,5,2)
			self.score += num
			self.block_blank.pop(index).new_color()
		except:
			print("end")
			self.app.running = False
	
	def render_number(self):
		for block in set(self.block_list) - set(self.block_blank):
			self.font.render_to(block.image,
										 (block.size//2-10*len(str(block.number)),block.size//2-10),
										 str(block.number),
										 (0,0,0))

	def render_score(self):
		#self.font.render_to(self.topic.image, (self.topic.image.get_width()//2 - 70, self.topic.image.get_height()//2-10), "Score {0}" .format(self.score), (0,0,0))
		self.font.render_to(self.app.screen, (self.app.WIDTH//2 - 70, 90), "Score {0}" .format(self.score), (0,0,0))

	def refresh_color(self):
		for block in self.block_list:
			block.new_color()

	def go(self, start, end):
		delta_x = end[0]-start[0]
		delta_y = end[1]-start[1]
		if abs(delta_x) + abs(delta_y) < 40:
			return 0
		for block in self.block_list:
			block.edited = False
		previos_blank = self.block_blank.copy()
		if abs(delta_x) > abs(delta_y):
			if delta_x > 0: #right
				a, b, c = 2, -1, -1
			else: #left
				a, b, c = 1, 4, 1
			self.make_go(a,b,c)
		else:
			if delta_y > 0: #bottom
				a, b, c = 2, -1, -1
			else: #up
				a, b, c = 1, 4, 1
			self.make_vert(a,b,c)
		is_change = self.set_blank()
		if is_change:
			self.refresh_color()
			self.generate_new()
	
	def set_blank(self):
		count = 0
		for i in range(len(self.block_blank)):
			if self.block_blank[i-count].number != 0:
				self.block_blank.pop(i-count)
				count += 1
		for block in self.block_list:
			if block.number == 0 and block not in self.block_blank:
					self.block_blank.append(block)
					count += 1
		return count != 0
	
	def make_go(self, a, b, c):
		for i in range(4):
			for j in range(a, b, c):
				if self.block_map[j][i] == 0:
					continue
				for k in range(j-c,3-b,-c):
					if self.we_can_add(i,i,k,k+c):
						self.set_edited(i,i,k,k+c)
						self.block_addition(i,i,k,k+c)
	
	def make_vert(self, a, b, c):
		for i in range(4):
			for j in range(a, b, c):
				if self.block_map[i][j] == 0:
					continue
				for k in range(j-c,3-b,-c):
					if self.we_can_add(k,k+c,i,i):
						self.set_edited(k,k+c,i,i)
						self.block_addition(k,k+c,i,i)

	def we_can_add(self, i, inext, k, next):
		return self.block_map[k][i].number == 0 or (self.block_map[k][i].number == self.block_map[next][inext].number and not self.block_map[k][i].edited and not self.block_map[next][inext].edited)
	
	def set_edited(self, i, inext, k, next):
		if self.block_map[k][i].number == 0:
			self.block_map[k][i].edited = self.block_map[next][inext].edited
		else:
			self.block_map[k][i].edited = True
		self.block_map[next][inext].edited = False

	def block_addition(self, i, inext, k,next):
		self.block_map[k][i].number += self.block_map[next][inext].number
		self.block_map[next][inext].number = 0