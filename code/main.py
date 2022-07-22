import pygame, sys
from pygame.math import Vector2 as vector
from settings import * 
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Cactus,Coffin

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = vector()
		self.display_surface = pygame.display.get_surface()
		self.bg = pygame.image.load('./graphics/other/bg.png').convert()

	def customize_draw(self, player):

		# Change the offset vector
		self.offset.x = player.rect.centerx - WINDOW_WIDTH // 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT // 2

		# Blit the surfaces
		self.display_surface.blit(self.bg,-self.offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_rect = sprite.image.get_rect(center = sprite.rect.center)
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image,offset_rect)

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Western shooter')
		self.clock = pygame.time.Clock()
		self.bullet_surf = pygame.image.load('./graphics/other/particle.png').convert_alpha()

		#  Groups
		self.all_sprites = AllSprites()
		self.obstacles = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()

		self.setup()
		self.music = pygame.mixer.Sound('./sound/music.mp3')
		self.music.play(loops=-1)

	def create_bullet(self,pos,direction):
		Bullet(pos,direction, self.bullet_surf, [self.all_sprites,self.bullets])

	def bullet_collision(self):

		# Bullet obstacle collision
		for obstacle in self.obstacles.sprites():
			pygame.sprite.spritecollide(obstacle,self.bullets,True, pygame.sprite.collide_mask)

		# Bullet monster collision
		for bullet in self.bullets.sprites():
			sprites = pygame.sprite.spritecollide(bullet,self.monsters,False, pygame.sprite.collide_mask)

			if sprites:
				bullet.kill()
				for sprite in sprites:
					sprite.damage()

		# Player bullet collision
		if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
			self.player.damage()

	def setup(self):
		tmx_map = load_pygame('./data/map.tmx')

		# Tile
		for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
			Sprite((x * 64,y * 64),surf,[self.all_sprites, self.obstacles])

		# Object
		for obj in tmx_map.get_layer_by_name('Objects'):
			Sprite((obj.x,obj.y),obj.image,[self.all_sprites, self.obstacles])

		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				self.player = Player(
					pos = (obj.x, obj.y),
					groups = self.all_sprites,
					path = PATHS['player'],
					collision_sprites = self.obstacles,
					create_bullet = self.create_bullet)

			if obj.name == 'Coffin':
				self.coffin = Coffin((obj.x, obj.y),[self.all_sprites,self.monsters],PATHS['coffin'],self.obstacles, self.player)

			if obj.name == 'Cactus':
				self.cactus = Cactus((obj.x, obj.y),[self.all_sprites,self.monsters],PATHS['cactus'],self.obstacles, self.player,self.create_bullet)

	def run(self):
		while True:
			# event loop 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick() / 1000
			
			# Update groups
			self.all_sprites.update(dt)
			self.bullet_collision()

			# Draw groups
			self.display_surface.fill('black')
			self.all_sprites.customize_draw(self.player)

			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()