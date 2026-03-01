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
        "anchovy":{"image":pygame.image.load("fish_placeholder1.png"), "sanity":1,"money":5, "percentage":14, "speed":1}, 
        "mackerel":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":1,"money":5, "percentage":14, "speed":2},
        "bass":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":1, "money":6, "percentage":12, "speed":1},
        "squid":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":2, "money":12, "percentage":10, "speed":3},
        "eel":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":3, "money":17, "percentage":9, "speed":2},
        "clownfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":4, "money":35, "percentage":8, "speed":1},
        "seahorse":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":5, "money":100, "percentage":8, "speed":5},
        "pufferfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":3, "money":20, "percentage":8, "speed":3},
        "butterflyfish":{"image":pygame.image.load("fish_uno.png"), "sanity":5, "money":110, "percentage":6, "speed":7},
        "napoleonfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":7, "money":250, "percentage":5, "speed":2},
        "tuna":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":10, "money":900, "percentage":2, "speed":1},
        "marlin":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":13, "money":1000, "percentage":1, "speed":1},
        "hammerhead":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":14, "money":1100, "percentage":1, "speed":3},
        "greatwhite":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":14, "money":1100, "percentage":1, "speed":5},
        "coelacanth":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":15, "money":1200, "percentage":1, "speed":1},
        }
    OBJECTS = {
        "A Spoon That Remembers Future Meals":{"image":pygame.image.load("spoon.png"), "sanity":-7, "money":400, "percentage":15, "speed":5},
        "An Equation Leaking Colour":{"image":pygame.image.load("spoon.png"), "sanity":-12, "money":900, "percentage":12, "speed":5},
        "The Sound of an Unsaid Apology":{"image":pygame.image.load("spoon.png"), "sanity":-10, "money":700, "percentage":13, "speed":5},
        "A Cube with Negative Volume":{"image":pygame.image.load("spoon.png"), "sanity":-60, "money":8000, "percentage":6, "speed":5},
        "Skeleton of a Fish":{"image":pygame.image.load("spoon.png"), "sanity":-3, "money":1, "percentage":25, "speed":5},
        "Half of a Whole That Doesn’t Exist Yet":{"image":pygame.image.load("spoon.png"), "sanity":-30, "money":5000, "percentage":5, "speed":5},
        "The Laughing Line Segment":{"image":pygame.image.load("spoon.png"), "sanity":-25, "money":1000, "percentage":10, "speed":5},
        "A Cube with Infinite Sides":{"image":pygame.image.load("spoon.png"), "sanity":-80, "money":10000, "percentage":2, "speed":5},
        "A Portrait of You Sorting Objects Before You Were Born":{"image":pygame.image.load("spoon.png"), "sanity":-99, "money":20000, "percentage":1, "speed":5},
        "Clock with Sixfold Hands":{"image":pygame.image.load("spoon.png"), "sanity":-20, "money":600, "percentage":15, "speed":5},
    }
    CHANCES = {"FISH":50, "OBJECTS":50}

    def weighted_pick(table):
        roll = random.randint(1, 100)
        cumulative = 0
        for name, info in table.items():
            cumulative += info["percentage"]
            if roll <= cumulative:
                return name
        return None
    
    def scale_to_fit(image, max_size):
        img_w, img_h = image.get_size()

        if img_w <= max_size[0] and img_h <= max_size[1]:
            return image

        scale = min(max_size[0] / img_w, max_size[1] / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        scaled_img = pygame.transform.smoothscale(image, new_size)
        return scaled_img

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

    class Resource():
        def __init__(self, type, x_pos, curr_amt):
            self.type = type
            self.x_pos = x_pos
            self.current_amount = curr_amt
        def display(self):
            font = pygame.font.Font(None, 35)
            line = f"{self.type.capitalize()}: {self.current_amount}"
            line_surface = font.render(line, True, (0,0,0))
            line_rect = line_surface.get_rect(topleft = (self.x_pos+5, 5))
            screen.blit(line_surface, line_rect)
    
    class Fish(pygame.sprite.Sprite):
        def __init__(self, type, fish_info):
            super().__init__()
            self.type = type
            self.image = scale_to_fit(fish_info["image"], (200,200))
            self.sanity = fish_info["sanity"]
            self.money = fish_info["money"]
            self.speed = fish_info["speed"]
            self.rect = self.image.get_rect(midleft=(1280, random.randint(400,720)))
        def update(self):
            self.rect.move_ip(-1 * self.speed, 0)
        @staticmethod
        def generate(FISH):
            fish_num = random.randint(1, 100)
            cumulative = 0
            gen_fish = None

            for name, fish in FISH.items():
                cumulative += fish["percentage"]
                if fish_num <= cumulative:
                    gen_fish = name
                    break
            return gen_fish
    
    class Object(pygame.sprite.Sprite):
        def __init__(self, type, obj_info):
            super().__init__()
            self.type = type
            self.image = scale_to_fit(obj_info["image"], (200,200))
            self.sanity = obj_info["sanity"]
            self.money = obj_info["money"]
            self.speed = obj_info["speed"]
            self.rect = self.image.get_rect(
                midleft=(1280, random.randint(400, 720))
            )

        def update(self):
            self.rect.move_ip(-self.speed, 0)

        @staticmethod
        def generate(OBJECTS):
            return weighted_pick(OBJECTS)
    
    
    def caught_display(name, scale):
        if name in FISH:
            original_image = FISH[name]["image"]
        else:
            original_image = OBJECTS[name]["image"]

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

    sanity = Resource("sanity", 5, 100)
    money = Resource("money", 175, 0)

    status = "game"
    entity_display = False
    caught_fish = None
    caught_frame = 0
    active_entities = pygame.sprite.Group()
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
                for entity in active_entities:
                    if entity.rect.collidepoint(event.pos):
                        if event.button == 1:
                            caught_frame = frame
                            caught_fish = entity.type
                            money.current_amount += entity.money
                            sanity.current_amount = min(100, sanity.current_amount + entity.sanity)
                            entity.kill()
                            entity.x = -2000
                            entity.kill()
                            entity_display = True
                        break
                    max_scale = 3.0
                    zooming = True
        pressed_keys = pygame.key.get_pressed()
        if status == "title":
            pass
        if status == "game":
            if frame % 300 == 0:
                category_roll = random.randint(1, 100)

                if category_roll <= CHANCES["FISH"]:
                    fish_type = weighted_pick(FISH)
                    if fish_type:
                        active_entities.add(Fish(fish_type, FISH[fish_type]))
                else:
                    obj_type = weighted_pick(OBJECTS)
                    if obj_type:
                        active_entities.add(Object(obj_type, OBJECTS[obj_type]))

            for entity in active_entities:
                entity.update()

            screen.fill((0,0,0))
            sea.update(screen)
            for entity in active_entities:
                screen.blit(entity.image, entity.rect)
            if entity_display:
                if frame <= caught_frame + 60:
                    image = pygame.image.load("effect.png").convert_alpha()
                    image_rect = image.get_rect(center=(640,360))
                    screen.blit(image, image_rect)
                    if max_scale > min_scale:
                        max_scale -= zoom_speed
                        if max_scale < min_scale:
                            max_scale = min_scale
                    caught_display(caught_fish, max_scale)
                else:
                    entity_display = False
                    max_scale = 1.0
            sanity.display()
            money.display()
            pygame.display.update()
            frame += 1
        
    
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()   


if __name__ == "__main__":
    asyncio.run(main())