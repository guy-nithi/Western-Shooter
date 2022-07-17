import pygame
from pygame.math import Vector2 as vector

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,path,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((100,100))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)

        # Float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 2000

        # Collisions
        self.hitbox = self.rect.inflate(0,-self.rect.height // 2)
        self.collision_sprites = collision_sprites