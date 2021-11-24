import pygame
from settings import *
from game import Game


class App():
	def __init__(self):
		pygame.init()
		info = pygame.display.Info()
		#self.WIDTH = info.current_w
		#self.HEIGHT = info.current_h
		self.WIDTH = 700
		self.HEIGHT = 1400
		self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
		pygame.display.set_caption("2048")
		self.clock = pygame.time.Clock()
		self.all_sprites = pygame.sprite.Group()
	
	def run(self):
		game = Game(self)
		game.generate_new()
		self.running = True
		while self.running:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					if game.score > game.record:
						with open('record.txt','w') as file:
							file.write(str(game.score))
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						pos = event.pos
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						end_pos = event.pos
						game.go(pos, end_pos)
			self.all_sprites.update()
			self.screen.fill(NOTHING)
			self.all_sprites.draw(self.screen)
			game.render_number()
			game.render_score()
			game.font.render_to(self.screen, (self.WIDTH//2 - 80, self.HEIGHT - 220), "Record {0}" .format(game.record), (0,0,0))
			pygame.display.flip()
			pygame.display.update()
		pygame.quit()