# Sprite classes for platform game
import pygame as pg
import pygame.gfxdraw
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("./img/astronaut_stand.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
 
    def jump(self):
        # Jump only if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
        self.image = pygame.image.load("./img/astronaut_jump.png")
        self.image.set_colorkey(BLACK)

    # Code that constantly runs at 60fps to update the player's position
    def update(self):
        if self.vel.y == 0:
            self.image = pygame.image.load("./img/astronaut_stand.png")
            self.image.set_colorkey(BLACK)
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # apply friction
        if self.rect.x < WIDTH * (2/3):
            self.acc.x += self.vel.x * PLAYER_FRICTION
        else:
            self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

            
        self.rect.midbottom = self.pos

# Creates a platform based on parameters
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# This doesn't work at the moment
class Planet(pg.sprite.Sprite):
    def __init__(self, x, y, r, c):
        pg.sprite.Sprite.__init__(self)
        self.ATOM_IMG = pygame.Surface((30, 30), pygame.SRCALPHA)
        pg.gfxdraw.aacircle(self.ATOM_IMG, x, y, r, c)
        pg.gfxdraw.filled_circle(self.ATOM_IMG, x, y, r, c)
        self.image = self.ATOM_IMG
        self.rect = self.image.get_rect(center=(150, 200))

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location