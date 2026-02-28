import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("bait")

clock = pygame.time.Clock()

def title():
    pass

def game():
    pass

def endscreen():
    pass


#MAIN

coins = 0

status = "title"

running = True

while running:
    for event in pygame.event.get(): 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()