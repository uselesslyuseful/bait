import pygame
from pygame.locals import *
import asyncio
import random

pygame.init()

async def main():

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("bait")
    FISH = {"tuna":{"image":pygame.image.load("fish_placeholder1.png"), "sanity":1,"money":1, "percentage":50}, "cod":{"image":pygame.image.load("fish_placeholder2.png"),"sanity":1,"money":1, "percentage":50}}

    class Sea:
        def __init__(self, images):
            self.images = images
            self.rects = [self.images[0].get_rect(topleft=(0,0)),self.images[1].get_rect(topleft=(1280,0)) ]
        def update(self, screen):
            for i in range(2):
                self.rects[i].move_ip(-1, 0)
                if self.rects[i].right <= 0:
                    other = self.rects[1-i]
                    self.rects[i].left = other.right-1

                screen.blit(self.images[i], self.rects[i])
    
    def fishing():
        fish_num = random.randint(1, 100)
        cumulative = 0
        caught_fish = None

        for name, fish in FISH.items():
            cumulative += fish["percentage"]
            if fish_num <= cumulative:
                caught_fish = name
                break
        return caught_fish
    
    def caught_fish_display(caught_fish):
        rect = FISH[caught_fish]["image"].get_rect(center=(640, 360))
        screen.blit(FISH[caught_fish]["image"], rect)

    clock = pygame.time.Clock()

    sea_images = [pygame.image.load("normal_sea.png"), pygame.image.load("normal_sea.png")]
    sea = Sea(sea_images)

    #MAIN

    coins = 0

    status = "game"
    fish_display = False
    caught_fish = None
    caught_frame = 0

    frame = 0
    running = True
    while running:
        for event in pygame.event.get(): 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and status == "game":
                caught_frame = frame
                if event.button == 1:
                    caught_fish = fishing()
                    fish_display = True
        pressed_keys = pygame.key.get_pressed()
        if status == "title":
            pass
        if status == "game":

            screen.fill((0,0,0))
            sea.update(screen)
            if fish_display:
                if frame <= caught_frame + 120:
                    caught_fish_display(caught_fish)
            pygame.display.update()
            frame += 1
    
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()   


if __name__ == "__main__":
    asyncio.run(main())