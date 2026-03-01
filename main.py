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
    FISH = {
        "anchovy":{"image":pygame.image.load("fish_placeholder1.png"), "sanity":1,"money":5, "percentage":13}, 
        "mackerel":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":1,"money":5, "percentage":13},
        "bass":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":1, "money":6, "percentage":12},
        "squid":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":2, "money":12, "percentage":10},
        "eel":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":3, "money":17, "percentage":9},
        "clownfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":4, "money":35, "percentage":8},
        "seahorse":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":5, "money":100, "percentage":8},
        "pufferfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":3, "money":20, "percentage":8},
        "butterflyfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":5, "money":110, "percentage":7},
        "napoleonfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":7, "money":250, "percentage":6},
        "tuna":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":10, "money":900, "percentage":2},
        "marlin":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":13, "money":1000, "percentage":1},
        "hammerhead":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":14, "money":1100, "percentage":1},
        "greatwhite":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":14, "money":1100, "percentage":1},
        "coelacanth":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":15, "money":1200, "percentage":1},
        }

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
    
    class Fish(pygame.sprite.Sprite):
        def __init__(self, fish_info):
            self.image = fish_info["image"]
            self.sanity = fish_info["sanity"]
            self.money = fish_info["money"]
            self.speed = fish_info["speed"]
            self.rect = self.image.get_rect(midright=(random.randint()))

    
    def create_fish():
        fish_num = random.randint(1, 100)
        cumulative = 0
        caught_fish = None

        for name, fish in FISH.items():
            cumulative += fish["percentage"]
            if fish_num <= cumulative:
                caught_fish = name
                break
        return caught_fish
    
    def caught_fish_display(caught_fish, scale):
        original_image = FISH[caught_fish]["image"]

        new_width = int(original_image.get_width() * scale)
        new_height = int(original_image.get_height() * scale)

        scaled_image = pygame.transform.smoothscale(
            original_image, (new_width, new_height)
        )

        rect = scaled_image.get_rect(center=(640, 360))
        screen.blit(scaled_image, rect)

    clock = pygame.time.Clock()

    sea_images = [pygame.image.load("normal_sea.png"), pygame.image.load("normal_sea.png")]
    sea = Sea(sea_images)

    #MAIN

    coins = 0

    status = "game"
    fish_display = False
    caught_fish = None
    caught_frame = 0
    active_fish = pygame.sprite.Group()
    max_scale = 3.0
    zoom_speed = 0.5
    min_scale = 1.0
    zooming = False

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
                for fish in active_fish:
                    if fish.rect.collidepoint(event.pos):
                        if event.button == 1:
                            caught_frame = frame
                            caught_fish = fish.type
                            fish_display = True
                        break
                    max_scale = 3.0
                    zooming = True
        pressed_keys = pygame.key.get_pressed()
        if status == "title":
            pass
        if status == "game":

            screen.fill((0,0,0))
            sea.update(screen)
            if fish_display:
                if frame <= caught_frame + 60:
                    image = pygame.image.load("effect.png").convert_alpha()
                    image_rect = image.get_rect(center=(640,360))
                    screen.blit(image, image_rect)
                    if max_scale > min_scale:
                        max_scale -= zoom_speed
                        if max_scale < min_scale:
                            max_scale = min_scale
                    caught_fish_display(caught_fish, max_scale)
                else:
                    fish_display = False
                    max_scale = 1.0
            pygame.display.update()
            frame += 1
    
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()   


if __name__ == "__main__":
    asyncio.run(main())