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
    GOALS = [500, 10000, 100000]
    FISH = {
        "anchovy":{"image":pygame.image.load("fish_cuatro.png"), "sanity":1,"money":5, "percentage":14, "speed":2}, 
        "mackerel":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":1,"money":5, "percentage":14, "speed":2},
        "bass":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":1, "money":6, "percentage":12, "speed":2},
        "squid":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":2, "money":12, "percentage":10, "speed":3},
        "totallyafish":{"image":pygame.image.load("fish_tres.png"), "sanity":3, "money":17, "percentage":9, "speed":2},
        "clownfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":4, "money":35, "percentage":8, "speed":2},
        "seahorse":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":5, "money":100, "percentage":8, "speed":5},
        "pufferfish":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":3, "money":20, "percentage":8, "speed":3},
        "bettafish":{"image":pygame.image.load("fish_uno.png"), "sanity":5, "money":110, "percentage":6, "speed":7},
        "sunfish":{"image":pygame.image.load("fish_dos.png"), "sanity":7, "money":250, "percentage":5, "speed":2},
        "tuna":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":10, "money":900, "percentage":2, "speed":2},
        "frog???":{"image":pygame.image.load("fish_cinco.png"), "sanity":13, "money":1000, "percentage":1, "speed":2},
        "hammerhead":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":14, "money":1100, "percentage":1, "speed":3},
        "greatwhite":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":14, "money":1100, "percentage":1, "speed":5},
        "coelacanth":{"image":pygame.image.load("fish_placeholder2.png"), "sanity":15, "money":1200, "percentage":1, "speed":1},
        }
    OBJECTS = {
        "A Spoon That Remembers Future Meals":{"image":pygame.image.load("spoon.png"), "sanity":-7, "money":400, "percentage":15, "speed":5},
        "An Equation Leaking Colour":{"image":pygame.image.load("equationleakingcolor.png"), "sanity":-12, "money":900, "percentage":11, "speed":5},
        "The Sound of an Unsaid Apology":{"image":pygame.image.load("condensedapology.png"), "sanity":-10, "money":700, "percentage":13, "speed":5},
        "A Cube with Negative Volume":{"image":pygame.image.load("tesseract.png"), "sanity":-60, "money":8000, "percentage":4, "speed":5},
        "Skeleton of a Fish":{"image":pygame.image.load("spoon.png"), "sanity":-3, "money":1, "percentage":25, "speed":5},
        "Half of a Whole That Doesn’t Exist Yet":{"image":pygame.image.load("halfofawholethatdoesntexistyet.png"), "sanity":-30, "money":5000, "percentage":5, "speed":5},
        "The Laughing Line Segment":{"image":pygame.image.load("spoon.png"), "sanity":-25, "money":1000, "percentage":10, "speed":5},
        "A Cube with Infinite Sides":{"image":pygame.image.load("squarewithinfinitesides.png"), "sanity":-80, "money":10000, "percentage":1, "speed":5},
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
    
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        return lines
    
    class TextBox(pygame.sprite.Sprite):
        def __init__(self, text):
            super().__init__()
            self.font = pygame.font.Font(None, 30)
            self.text = text
            self.image = pygame.image.load("box.png")
            self.rect = self.image.get_rect(center=(640, 620))
            self.curr_text = 0
        def draw(self):
            screen.blit(self.image, self.rect)
            lines = wrap_text(self.text[self.curr_text], self.font, 900)
            y = 590
            for line in lines:
                text_surface = self.font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(640, y))
                screen.blit(text_surface, text_rect)
                y += 30
        def update(self):
            self.curr_text += 1

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
            if self.rect.right < 0:
                self.kill()
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

        new_width = int(scale_to_fit(original_image, (500,400)).get_width() * scale)
        new_height = int(scale_to_fit(original_image, (500,400)).get_height() * scale)

        scaled_image = pygame.transform.smoothscale(
            original_image, (new_width, new_height)
        )

        rect = scaled_image.get_rect(center=(640, 360))
        screen.blit(scaled_image, rect)

    clock = pygame.time.Clock()

    sea_images = [pygame.image.load("normal_sea.png"), pygame.image.load("normal_sea.png")]
    sea = Sea(sea_images)

    title_image = pygame.image.load("title_screen.png")
    effect_image = pygame.image.load("effect.png").convert_alpha()

    #MAIN

    sanity = Resource("sanity", 5, 100)
    money = Resource("money", 175, 0)

    status = "title"
    tutorial_phase = "dialogue"
    tutorial_fish_spawned = False
    entity_display = False
    caught_fish = None
    caught_frame = 0
    active_entities = pygame.sprite.Group()
    max_scale = 3.0
    zoom_speed = 0.5
    min_scale = 1.0
    zooming = False
    level = 0
    tutorial_text = ["Welcome to Bait!",
                            "In this tutorial, you'll learn how to catch your own fish.",
                            "After this dialogue, you'll see a fish show up.",
                            "Click on it to catch it!",
                            "Good job!",
                            "You caught your fish! That's all you need to play the game :D",
                            "Different fish are worth different amounts of money, and have different spawn rates.",
                            "You ready?",
                            "Oh, you're asking about the sanity bar?",
                            "...Don't worry about it.",
                            "Now, get to fishing!"]
    second_tutorial = ["By now, you're surely curious about the sanity bar.",
                        "I think you're ready.",
                        "Let's introduce you to the other catches.",
                        "What you're about to see...",
                        "Well.",
                        "Don't go insane, yeah?",
                        "So you survived catching that.",
                        "Good for you! Many others have failed.",
                        "You might notice your sanity has decreased.",
                        "These... objects. They'll have much higher coin values, but they'll also cost you heavily in sanity.",
                        "Watch out. Some of them will take as much as they can.",
                        "Replenish your sanity by catching normal fish.",
                        "Good luck."]
    text_box = TextBox(tutorial_text)

    frame = 0
    start = True
    running = True


    while running:
        for event in pygame.event.get(): 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_RETURN and status == "title":
                    status = "tutorial"
                elif event.key == K_RETURN and (status == "tutorial" or status == "second_tutorial"):
                    if tutorial_phase == "dialogue":
                        if (
                            (status == "tutorial" and text_box.curr_text < 3) or
                            (status == "second_tutorial" and text_box.curr_text < 5)
                        ):
                            text_box.update()
                        else:
                            tutorial_phase = "catch"
                            text_box.kill()
                    elif tutorial_phase == "post_dialogue":
                        current_script = tutorial_text if status == "tutorial" else second_tutorial

                        if text_box.curr_text < len(current_script) - 1:
                            text_box.update()
                        else:
                            status = "game"
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and status in ("game", "tutorial", "second_tutorial"):
                for entity in active_entities:
                    if entity.rect.collidepoint(event.pos):
                        if event.button == 1:
                            caught_frame = frame
                            caught_fish = entity.type
                            money.current_amount += entity.money
                            sanity.current_amount = min(100, sanity.current_amount + entity.sanity)
                            entity.rect.x = -2000
                            entity.kill()
                            entity_display = True
                            max_scale = 3.0
                            if status == "tutorial" and tutorial_phase == "catch":
                                tutorial_phase = "post_dialogue"
                                text_box.curr_text = 4
                                entity_display = False
                                max_scale = 1.0
                            elif status == "second_tutorial" and tutorial_phase =="catch":
                                tutorial_phase = "post_dialogue"
                                text_box.curr_text = 6
                                entity_display = False
                                max_scale = 1.0
                        break
        pressed_keys = pygame.key.get_pressed()
        if status == "title":
            screen.blit(title_image,(0,0))
        elif status == "tutorial":
            screen.fill((0,0,0))
            sea.update(screen)

            if tutorial_phase == "dialogue":
                text_box.draw()
            elif tutorial_phase == "catch":
                if len(active_entities) == 0:
                    active_entities.add(Fish("anchovy", FISH["anchovy"]))

                for entity in active_entities:
                    entity.update()
                    pygame.draw.rect(screen, (255,255,0), entity.rect.inflate(10,10), 2)
                    screen.blit(entity.image, entity.rect)
            elif tutorial_phase == "post_dialogue":
                text_box.draw()
            sanity.display()
            money.display()
        elif status == "second_tutorial":
            if start:
                text_box = TextBox(second_tutorial)
                tutorial_phase = "dialogue"
                active_entities.empty()
                start = False
            screen.fill((0,0,0))
            sea.update(screen)
            if tutorial_phase == "dialogue":
                text_box.draw()
            elif tutorial_phase == "catch":
                if len(active_entities) == 0:
                    active_entities.add(Object("A Spoon That Remembers Future Meals", OBJECTS["A Spoon That Remembers Future Meals"]))
                for entity in active_entities:
                    entity.update()
                    pygame.draw.rect(screen, (255,0,0), entity.rect.inflate(10,10), 2)
                    screen.blit(entity.image, entity.rect)
            elif tutorial_phase == "post_dialogue":
                text_box.draw()
            sanity.display()
            money.display()
        elif status == "game":
            goal = GOALS[level]
            font = pygame.font.Font(None, 35)
            goal_text = f"Goal: {goal}"
            goal_surface = font.render(goal_text, True, (0,0,0))
            goal_rect = goal_surface.get_rect(topright = (1270, 5))

            if goal != "???" and money.current_amount >= goal:
                if level >= len(GOALS):
                    goal = "???"
                else:
                    level += 1
                    if level == 1:
                        status = "second_tutorial"

            if frame % 300 == 0:
                category_roll = random.randint(1, 100)

                if level == 0:
                    fish_type = weighted_pick(FISH)
                    if fish_type:
                        active_entities.add(Fish(fish_type, FISH[fish_type]))
                else:
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
                    image_rect = effect_image.get_rect(center=(640,360))
                    screen.blit(effect_image, image_rect)
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
            screen.blit(goal_surface, goal_rect)
            frame += 1

        clock.tick(60)
        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()   


if __name__ == "__main__":
    asyncio.run(main())