# Pygame template - skeleton for new pygame project
import pygame
import random
from settings import *

# initialize pygmae and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    # Check for events that have happened since last time this line was run
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()