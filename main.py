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
    GOALS = [50, 10000, 100000]
    FISH = {
        "anchovy":{"image":pygame.image.load("fish_cuatro.png"), "sanity":1,"money":5, "percentage":40, "speed":2}, 
        "totallyafish":{"image":pygame.image.load("fish_tres.png"), "sanity":3, "money":17, "percentage":20, "speed":2},
        "goldfish":{"image":pygame.image.load("fih_seis.png"), "sanity":4, "money":35, "percentage":16, "speed":2},
        "shrimp":{"image":pygame.image.load("fih_siete_shrih.png"), "sanity":5, "money":100, "percentage":14, "speed":5},
        "bettafish":{"image":pygame.image.load("fish_uno.png"), "sanity":5, "money":210, "percentage":5, "speed":7},
        "sunfish":{"image":pygame.image.load("fish_dos.png"), "sanity":7, "money":350, "percentage":4, "speed":2},
        "frog???":{"image":pygame.image.load("fish_cinco.PNG"), "sanity":13, "money":1500, "percentage":1, "speed":2},
        }
    OBJECTS = {
        "A Spoon That Remembers Future Meals":{"image":pygame.image.load("spoon.png"), "sanity":-7, "money":400, "percentage":15, "speed":5},
        "An Equation Leaking Colour":{"image":pygame.image.load("equationleakingcolor.png"), "sanity":-12, "money":900, "percentage":11, "speed":5},
        "The Sound of an Unsaid Apology":{"image":pygame.image.load("condensedapology.png"), "sanity":-10, "money":700, "percentage":13, "speed":5},
        "A Cube with Negative Volume":{"image":pygame.image.load("tesseract.png"), "sanity":-60, "money":8000, "percentage":4, "speed":5},
        "Skeleton of a Fish":{"image":pygame.image.load("skeletonfish.png"), "sanity":-3, "money":1, "percentage":25, "speed":5},
        "Half of a Whole That Doesn’t Exist Yet":{"image":pygame.image.load("halfofawholethatdoesntexistyet.png"), "sanity":-30, "money":5000, "percentage":5, "speed":5},
        "The Laughing Line Segment":{"image":pygame.image.load("laughinglinesegment.png"), "sanity":-25, "money":1000, "percentage":10, "speed":5},
        "A Cube with Infinite Sides":{"image":pygame.image.load("squarewithinfinitesides.png"), "sanity":-80, "money":10000, "percentage":1, "speed":5},
        "A Portrait of You Fishing Before You Were Born":{"image":pygame.image.load("portrait.png"), "sanity":-99, "money":20000, "percentage":1, "speed":5},
        "Clock with Sixfold Hands":{"image":pygame.image.load("sixfoldclock.png"), "sanity":-20, "money":600, "percentage":15, "speed":5},
    }
    chances = {"FISH":50, "OBJECTS":50}

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
    
    class Button:
        def __init__(self, image, text, center_pos, price=None, size=120):
            self.image = pygame.image.load(image)
            self.text = text
            self.price = price
            self.size = size
            self.font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 24)

            self.rect = self.image.get_rect(center=center_pos)

        def draw(self, screen):
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, (80, 80, 80), self.rect, 3)

            label = self.font.render(self.text, True, (0, 0, 0))
            label_rect = label.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 6))
            screen.blit(label, label_rect)

            if self.price is not None:
                price_text = self.small_font.render(f"${self.price}", True, (0, 120, 0))
                price_rect = price_text.get_rect(midtop=(self.rect.centerx, label_rect.bottom + 2))
                screen.blit(price_text, price_rect)

        def clicked(self, pos):
            return self.rect.collidepoint(pos)

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
        def set_images(self, images):
            self.images = images

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
            img_w, img_h = self.image.get_size()
            min_top = 260
            max_top = 720 - img_h

            y_pos = random.randint(min_top, max_top)
            self.rect = self.image.get_rect(topleft=(1280, y_pos))
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
            img_w, img_h = self.image.get_size()
            min_top = 260
            max_top = 720 - img_h

            y_pos = random.randint(min_top, max_top)
            self.rect = self.image.get_rect(topleft=(1280, y_pos))

        def update(self):
            self.rect.move_ip(-self.speed, 0)

        @staticmethod
        def generate(OBJECTS):
            return weighted_pick(OBJECTS)

    class StationMenu():
        def __init__(self, screen_width, screen_height, attributes_dict):
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.attributes_dict = attributes_dict

            self.preview_cache = {}

            for category in self.attributes_dict.values():
                for name, info in category.items():
                    self.preview_cache[name] = pygame.transform.smoothscale(info["image"], (60, 60))

            self.button_size = 80
            self.button_image = pygame.image.load("dictionary.png")
            self.button_rect = self.button_image.get_rect(center=(screen_width - self.button_size//2 - 10, 100))

            self.popup_width = 900
            self.popup_height = 600
            self.popup_rect = pygame.Rect((screen_width - self.popup_width)//2, (screen_height - self.popup_height)//2, self.popup_width, self.popup_height)

            self.close_rect = pygame.Rect(self.popup_rect.right - 35, self.popup_rect.top + 10, 30, 30)

            self.stations = ["fish", "objects"]
            self.station_buttons = []
            self._generate_station_buttons()
            
            self.open = False
            self.active_station = None
            
            self.scroll_offset = 0
            self.scroll_offset_minmax = (-500, 20)
            self.scroll_speed = 20

            self.font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 22)

        def _generate_station_buttons(self):
            btn_width = self.popup_width // len(self.stations)
            btn_height = 60
            y = self.popup_rect.top + 50

            for i, station in enumerate(self.stations):
                rect = pygame.Rect(self.popup_rect.left + (i * btn_width), y, btn_width, btn_height)
                self.station_buttons.append((station, rect))
        
        def toggle(self):
            self.open = not self.open
            self.active_station = None
            self.scroll_offset = 0
        
        def handle_event(self, event):

            if not self.open:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        self.toggle()
                return
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.close_rect.collidepoint(event.pos):
                    self.toggle()
                    return
                
                for station, rect in self.station_buttons:
                    if rect.collidepoint(event.pos):
                        self.active_station = station
                        self.scroll_offset = 0
                        self._update_scroll_limits()
                        return
                
            if event.type == MOUSEWHEEL:
                self.scroll_offset += event.y * self.scroll_speed
                self.scroll_offset = max(min(self.scroll_offset_minmax[1], self.scroll_offset), self.scroll_offset_minmax[0])

                
            
        def draw(self, screen):
            if not self.open:
                pygame.draw.rect(screen, (100, 100, 100), self.button_rect.inflate(4,4), 4)
                screen.blit(self.button_image, self.button_rect)
                return
            
            pygame.draw.rect(screen, (12, 105, 95), self.popup_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.popup_rect, 4)

            pygame.draw.rect(screen, (200, 50, 50), self.close_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.close_rect, 2)

            for station, rect in self.station_buttons:
                color = (90, 90, 80) if station == self.active_station else (130, 130, 130)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)

                label = self.small_font.render(station.replace("_", " ").title(), True, (255, 255, 255))
                screen.blit(label, label.get_rect(center = rect.center))
            
            if self.active_station:
                self._draw_tag_list(screen)

        def _draw_tag_list(self, screen):
            clip_rect = pygame.Rect(
                self.popup_rect.left + 20,
                self.popup_rect.top + 120,
                self.popup_width - 40,
                self.popup_height - 160
            )

            screen.set_clip(clip_rect)

            y = clip_rect.top + self.scroll_offset
            x = clip_rect.left + 10

            entries = self.attributes_dict[self.active_station]

            for name, info in entries.items():
                img = self.preview_cache[name]
                img_rect = img.get_rect(topleft=(x, y))
                screen.blit(img, img_rect)

                name_surface = self.font.render(name.title(), True, (159, 209, 196))
                screen.blit(name_surface, (x + 80, y))

                attr_y = y + 28

                for key, value in info.items():
                    if key == "image":
                        continue

                    attr_surface = self.small_font.render(
                        f"{key.capitalize()}: {value}", True, (220, 220, 220)
                    )
                    screen.blit(attr_surface, (x + 80, attr_y))
                    attr_y += 20
                y += max(80, attr_y - y) + 10

            screen.set_clip(None)
        
        def _update_scroll_limits(self):
            if not self.active_station:
                return

            entries = self.attributes_dict[self.active_station]
            content_height = len(entries) * 120

            visible_height = self.popup_height - 160
            min_scroll = min(0, visible_height - content_height)

            self.scroll_offset_minmax = (min_scroll, 20)
    
    
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

    normal_sea_imgs = [
    pygame.image.load("normal_sea.png"),
    pygame.image.load("normal_sea.png")
    ]
    mild_sea_imgs = [
        pygame.image.load("mild_insanity_sea.png"),
        pygame.image.load("mild_insanity_sea.png")
    ]
    high_sea_imgs = [
        pygame.image.load("high_insanity_sea.png"),
        pygame.image.load("high_insanity_sea.png")
    ]

    sea = Sea(normal_sea_imgs)
    current_sea_state = "normal"

    title_image = pygame.image.load("title_screen.png")
    effect_image = pygame.image.load("effect.png").convert_alpha()

    #MAIN

    sanity = Resource("sanity", 5, 100)
    money = Resource("money", 175, 0)

    status = "tutorial"
    tutorial_phase = "dialogue"
    tutorial_fish_spawned = False
    entity_display = False
    caught_fish = None
    caught_frame = 0
    spawn_rate = 300
    active_entities = pygame.sprite.Group()
    max_scale = 3.0
    zoom_speed = 0.5
    min_scale = 1.0
    fisher_image = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load("fisher.png").convert_alpha(), (250, 150)), -15)
    fisher_rect = fisher_image.get_rect(center=(640, 175))
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
    ending_text = ["Well.",
                    "I suppose you tried your best.",
                    "I don't blame you. Many stronger have also lost their minds.",
                    "A shame that you'll die here.",
                    "Don't worry, you'll be replaced soon enough.",
                    "...Goodbye.",]
    text_box = TextBox(tutorial_text)
    shop_button = Button("shop.png", "Shop", (50, 100), size=80)
    spawn_rate_plus = Button("spawnup.png","Spawn Faster", (350, 220), price=20)
    spawn_rate_minus = Button("spawndown.png","Spawn Slower", (930, 220), price=20)
    object_rate_plus = Button("objectup.png","More Objects", (350, 420), price=50)
    object_rate_minus = Button("objectdown.png","Fewer Objects", (930, 420), price=50)
    shop_message = ""
    shop_message_timer = 0

    station_data = {
        "fish": FISH,
        "objects": OBJECTS
    }

    station_menu = StationMenu(SCREEN_WIDTH, SCREEN_HEIGHT, station_data)
    

    frame = 0
    start = True
    running = True


    while running:
        for event in pygame.event.get():
            station_menu.handle_event(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_x and status == "shop":
                    status = "game"
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
                elif event.key == K_RETURN and status == "end":

                    if text_box.curr_text < len(ending_text) - 1:
                        text_box.update()
                    else:
                        running = False
            elif event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and status in ("game", "tutorial", "second_tutorial", "shop"):
                if status == "game":
                    if shop_button.clicked(event.pos):
                        status = "shop"
                        continue
                    for entity in active_entities:
                        if entity.rect.collidepoint(event.pos):
                            if event.button == 1:
                                caught_frame = frame
                                caught_fish = entity.type
                                money.current_amount += entity.money
                                sanity.current_amount = min(100, sanity.current_amount + entity.sanity)
                                if sanity.current_amount < 25:
                                    desired_state = "high"
                                elif sanity.current_amount < 50:
                                    desired_state = "mild"
                                else:
                                    desired_state = "normal"

                                if desired_state != current_sea_state:
                                    current_sea_state = desired_state

                                    if desired_state == "high":
                                        sea.set_images(high_sea_imgs)
                                    elif desired_state == "mild":
                                        sea.set_images(mild_sea_imgs)
                                    else:
                                        sea.set_images(normal_sea_imgs)
                                entity.rect.x = -2000
                                entity.kill()
                                if sanity.current_amount <= 0:
                                    status = "end"
                                    start = True
                                    break
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

                elif status in ("tutorial", "second_tutorial"):
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

                elif status == "shop":

                    close_button_rect = pygame.Rect(
                        SCREEN_WIDTH - 40,
                        10,
                        30,
                        30
                    )

                    if close_button_rect.collidepoint(event.pos):
                        status = "game"
                        shop_message_timer = 0
                        continue

                    if spawn_rate_plus.clicked(event.pos):
                        if money.current_amount >= spawn_rate_plus.price:
                            money.current_amount -= spawn_rate_plus.price
                            spawn_rate -= 5
                        else:
                            shop_message = "You don't have enough money!"
                            shop_message_timer = 80
                    elif spawn_rate_minus.clicked(event.pos):
                        if money.current_amount >= spawn_rate_minus.price:
                            money.current_amount -= spawn_rate_minus.price
                            spawn_rate += 5
                        else:
                            shop_message = "You don't have enough money!"
                            shop_message_timer = 80
                    elif object_rate_plus.clicked(event.pos):
                        if money.current_amount >= object_rate_plus.price:
                            money.current_amount -= object_rate_plus.price
                            chances["FISH"] -= 5
                            chances["OBJECTS"] += 5
                        else:
                            shop_message = "You don't have enough money!"
                            shop_message_timer = 80
                    elif object_rate_minus.clicked(event.pos):
                        if money.current_amount >= object_rate_minus.price:
                            money.current_amount -= object_rate_minus.price
                            chances["FISH"] += 5
                            chances["OBJECTS"] -= 5
                        else:
                            shop_message = "You don't have enough money!"
                            shop_message_timer = 80

                    money.display()

                    if shop_message_timer > 0:
                        font_small = pygame.font.Font(None, 40)
                        warning = font_small.render(shop_message, True, (255, 80, 80))
                        warning_rect = warning.get_rect(center=(640, 360))
                        screen.blit(warning, warning_rect)

                        shop_message_timer -= 1


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
            screen.blit(fisher_image, fisher_rect)
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
            screen.blit(fisher_image, fisher_rect)
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

            if frame % spawn_rate == 0:
                category_roll = random.randint(1, 100)

                if level == 0:
                    fish_type = weighted_pick(FISH)
                    if fish_type:
                        active_entities.add(Fish(fish_type, FISH[fish_type]))
                else:
                    if category_roll <= chances["FISH"]:
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
            shop_button.draw(screen)
            station_menu.draw(screen)
            screen.blit(goal_surface, goal_rect)
            screen.blit(fisher_image, fisher_rect)
            frame += 1
        
        elif status == "shop":

            screen.fill((100, 227, 214))

            close_button_rect = pygame.Rect(
                        SCREEN_WIDTH - 50,
                        10,
                        40,
                        40
                    )

            pygame.draw.rect(screen, (180, 60, 60), close_button_rect)
            pygame.draw.line(screen, (255,255,255), close_button_rect.topleft, close_button_rect.bottomright, 2)
            pygame.draw.line(screen, (255,255,255), close_button_rect.topright, close_button_rect.bottomleft, 2)

            font = pygame.font.Font(None, 60)
            title = font.render("SHOP", True, (0, 0, 0))
            screen.blit(title, title.get_rect(center=(640, 100)))

            spawn_rate_plus.draw(screen)
            spawn_rate_minus.draw(screen)
            object_rate_plus.draw(screen)
            object_rate_minus.draw(screen)

            money.display()

            if shop_message_timer > 0:
                font_small = pygame.font.Font(None, 40)
                warning = font_small.render(shop_message, True, (255, 80, 80))
                warning_rect = warning.get_rect(center=(640, 320))
                screen.blit(warning, warning_rect)

                shop_message_timer -= 1
        elif status == "end":
            if start:
                text_box = TextBox(ending_text)
                start = False
            sea.update(screen)
            text_box.draw()

        clock.tick(60)
        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()   


if __name__ == "__main__":
    asyncio.run(main())