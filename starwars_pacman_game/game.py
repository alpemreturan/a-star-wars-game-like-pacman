import pygame
import os
import sys
from collections import deque

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Star Wars")

if getattr(sys, 'frozen', False):
    current_dir = sys._MEIPASS
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(current_dir, "config.txt")
assets_path = os.path.join(current_dir, "Assets")
click_sound_path = os.path.join(current_dir, "click.mp3")
effect_sound_path = os.path.join(current_dir, "effect.mp3")
music_path = os.path.join(current_dir, "music.mp3")
victory_sound_path = os.path.join(current_dir, "victory.mp3")
icon_path = os.path.join(current_dir, "icon.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

FPS = 60

def load_map(config_path):
    grid = []
    with open(config_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip().startswith('Character') and not line.strip().startswith('Door') and line.strip():
                grid.append([int(x) for x in line.strip().split('\t')])
    return grid

grid = load_map(config_path)

GRID_SIZE = 50
GRID_WIDTH = len(grid[0])
GRID_HEIGHT = len(grid)

CHARACTER_WIDTH = GRID_SIZE
CHARACTER_HEIGHT = GRID_SIZE

class Location:
    def __init__(self, char_x, char_y):
        self.char_x = char_x
        self.char_y = char_y

    def set_x(self, new_x):
        self.char_x = new_x
    
    def set_y(self, new_y):
        self.char_y = new_y
        
    def get_x(self):
        return self.char_x
    
    def get_y(self):
        return self.char_y

class Character:
    def __init__(self, name, type_, location):
        self.name = name
        self.type_ = type_
        self.location = location

    def move(self, direction, grid):
        new_x, new_y = self.location.char_x, self.location.char_y
        if direction == "left" and new_x > 0 and grid[new_y][new_x - 1] == 1:
            new_x -= 1
        elif direction == "right" and new_x < GRID_WIDTH - 1 and grid[new_y][new_x + 1] == 1:
            new_x += 1
        elif direction == "up" and new_y > 0 and grid[new_y - 1][new_x] == 1:
            new_y -= 1
        elif direction == "down" and new_y < GRID_HEIGHT - 1 and grid[new_y + 1][new_x] == 1:
            new_y += 1
        self.location.set_x(new_x)
        self.location.set_y(new_y)

    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    def get_type(self):
        return self.type_
    
    def set_type(self, new_type):
        self.type_ = new_type

    def get_position(self):
        return self.location.get_x(), self.location.get_y()
    
    def set_position(self, new_position):
        self.location.set_x(new_position[0])
        self.location.set_y(new_position[1])

    def show_info(self):
        return f"Character Name: {self.name}, Type: {self.type_}, Position: {self.get_position()}"

class MasterYoda(Character):
    def __init__(self, name, type_, location, health):
        super().__init__(name, type_, location)
        self.health = health

    def decrease_health(self):
        self.health = max(self.health - 0.5, 0)

    def set_health(self, new_health):
        self.health = new_health

    def get_health(self):
        return self.health

class LukeSkywalker(Character):
    def __init__(self, name, type_, location, health):
        super().__init__(name, type_, location)
        self.health = health

    def decrease_health(self):
        self.health = max(self.health - 1, 0)

    def set_health(self, new_health):
        self.health = new_health

    def get_health(self):
        return self.health

class DarthVader(Character):
    def __init__(self, name, type_, location):
        super().__init__(name, type_, location)

    def shortest_path(self, target, grid):
        def bfs(start, goal):
            queue = deque([start])
            visited = set()
            parents = {start: None}

            while queue:
                current = queue.popleft()
                visited.add(current)

                if current == goal:
                    path = []
                    while current:
                        path.append(current)
                        current = parents[current]
                    return path[::-1]

                x, y = current
                neighbors = [
                    (x - 1, y), (x + 1, y),
                    (x, y - 1), (x, y + 1) 
                ]

                for nx, ny in neighbors:
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in visited:
                        parents[(nx, ny)] = current
                        queue.append((nx, ny))
            return []

        start = (self.location.char_x, self.location.char_y)
        goal = (target.location.char_x, target.location.char_y)

        return bfs(start, goal)

class KyloRen(Character):
    def __init__(self, name, type_, location):
        super().__init__(name, type_, location)

    def shortest_path(self, target, grid):
        def bfs(start, goal):
            queue = deque([start])
            visited = set()
            parents = {start: None}

            while queue:
                current = queue.popleft()
                visited.add(current)

                if current == goal:
                    path = []
                    while current:
                        path.append(current)
                        current = parents[current]
                    return path[::-1]

                x, y = current
                neighbors = [
                    (x - 1, y), (x + 1, y),
                    (x, y - 1), (x, y + 1)
                ]

                for nx, ny in neighbors:
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 1 and (nx, ny) not in visited:
                        parents[(nx, ny)] = current
                        queue.append((nx, ny))
            return []

        start = (self.location.char_x, self.location.char_y)
        goal = (target.location.char_x, target.location.char_y)
        return bfs(start, goal)

class Stormtrooper(Character):
    def __init__(self, name, type_, location):
        super().__init__(name, type_, location)

    def shortest_path(self, target, grid):
        def bfs(start, goal):
            queue = deque([start])
            visited = set()
            parents = {start: None}

            while queue:
                current = queue.popleft()
                visited.add(current)

                if current == goal:
                    path = []
                    while current:
                        path.append(current)
                        current = parents[current]
                    return path[::-1]

                x, y = current
                neighbors = [
                    (x - 1, y), (x + 1, y),
                    (x, y - 1), (x, y + 1)
                ]

                for nx, ny in neighbors:
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 1 and (nx, ny) not in visited:
                        parents[(nx, ny)] = current
                        queue.append((nx, ny))
            return []

        start = (self.location.char_x, self.location.char_y)
        goal = (target.location.char_x, target.location.char_y)
        return bfs(start, goal)

master_yoda = MasterYoda("Master Yoda", "good", Location(6, 5), 3)
luke_skywalker = LukeSkywalker("Luke Skywalker", "good", Location(6, 5), 3)

stormtrooper_start_positions = {}
storm_troopers = []

kyloren_start_positions = {}
kylo_rens = []

darth_vader_start_positions = {}
darth_vaders = []

with open("config.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    if "Character:" in line and "Door:" in line:
        parts = line.split(",")
        character_info = parts[0].split(":")[1].strip()
        door_info = parts[1].split(":")[1].strip()

        if door_info == "A":
            door_x, door_y = 0, 5
        elif door_info == "B":
            door_x, door_y = 4, 0
        elif door_info == "C":
            door_x, door_y = 12, 0
        elif door_info == "D":
            door_x, door_y = 13, 5
        elif door_info == "E":
            door_x, door_y = 4, 10

        if character_info == "Stormtrooper":
            stormtrooper_id = len(storm_troopers)
            storm_trooper = Stormtrooper(f"Stormtrooper_{stormtrooper_id}", "evil", Location(door_x, door_y))
            storm_troopers.append(storm_trooper)
            stormtrooper_start_positions[stormtrooper_id] = (door_x, door_y)

        elif character_info == "Kyloren":
            kylo_ren_id = len(kylo_rens)
            kylo_ren = KyloRen(f"KyloRen_{kylo_ren_id}", "evil", Location(door_x, door_y))
            kylo_rens.append(kylo_ren)
            kyloren_start_positions[kylo_ren_id] = (door_x, door_y)
        
        elif character_info == "Darthvader":
            darth_vader_id = len(darth_vaders)
            darth_vader = DarthVader(f"DarthVader_{darth_vader_id}", "evil", Location(door_x, door_y))
            darth_vaders.append(darth_vader)
            darth_vader_start_positions[darth_vader_id] = (door_x, door_y)

MASTER_YODA_IMAGE = pygame.image.load(os.path.join(assets_path, "masteryoda.png"))
MASTER_YODA = pygame.transform.scale(MASTER_YODA_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

LUKE_SKYWALKER_IMAGE = pygame.image.load(os.path.join(assets_path, "lukeskywalker.png"))
LUKE_SKYWALKER = pygame.transform.scale(LUKE_SKYWALKER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

STORMTROOPER_IMAGE = pygame.image.load(os.path.join(assets_path, "stormtrooper.png"))
STORMTROOPER = pygame.transform.scale(STORMTROOPER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

KYLO_REN_IMAGE = pygame.image.load(os.path.join(assets_path, "kyloren.png"))
KYLO_REN = pygame.transform.scale(KYLO_REN_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

DARTH_VADER_IMAGE = pygame.image.load(os.path.join(assets_path, "darthvader.png"))
DARTH_VADER = pygame.transform.scale(DARTH_VADER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

TROPHY_IMAGE = pygame.image.load(os.path.join(assets_path, "trophy.png"))
TROPHY = pygame.transform.scale(TROPHY_IMAGE, (CHARACTER_WIDTH + 20, CHARACTER_HEIGHT + 10))

OK_IMAGE = pygame.image.load(os.path.join(assets_path, "ok.png"))
OK = pygame.transform.scale(OK_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

LOGO_IMAGE = pygame.image.load(os.path.join(assets_path, "logo.png"))
LOGO = pygame.transform.scale(LOGO_IMAGE, (400, 200))

HALF_IMAGE = pygame.image.load(os.path.join(assets_path, "half.png"))
HALF = pygame.transform.scale(HALF_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

HEART_IMAGE = pygame.image.load(os.path.join(assets_path, "heart.png"))
HEART = pygame.transform.scale(HEART_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

ROTATED_OK_90 = pygame.transform.rotate(OK, 90)
ROTATED_OK_180 = pygame.transform.rotate(OK, 180)
ROTATED_OK_270 = pygame.transform.rotate(OK, 270)

GRID_PIXEL_WIDTH = GRID_WIDTH * GRID_SIZE
GRID_PIXEL_HEIGHT = GRID_HEIGHT * GRID_SIZE

OFFSET_X = (SCREEN_WIDTH - GRID_PIXEL_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - GRID_PIXEL_HEIGHT) // 2

original_grid = [row[:] for row in grid]

luke_skywalker_start_char_x = 6
luke_skywalker_start_char_y = 5

master_yoda_start_char_x = 6
master_yoda_start_char_y = 5

def draw_screen(character):
    SCREEN.fill((173, 216, 230))

    label_positions = {
        (0, 5): "A",
        (4, 0): "B",
        (12, 0): "C",
        (13, 5): "D",
        (4, 10): "E",
    }

    font = pygame.font.Font(None, 24)

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            value = grid[row][col]

            label = label_positions.get((col, row))
            if label:
                color = "DARKBLUE"
            elif value == 1:
                color = (173, 216, 230)
            else:
                color = "WHITE"

            rect_x = OFFSET_X + col * GRID_SIZE
            rect_y = OFFSET_Y + row * GRID_SIZE
 
            pygame.draw.rect(SCREEN, color, (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(SCREEN, "DARK GRAY", (rect_x, rect_y, GRID_SIZE, GRID_SIZE), 1)
    
    rect_x = OFFSET_X + luke_skywalker_start_char_x * GRID_SIZE
    rect_y = OFFSET_Y + luke_skywalker_start_char_y * GRID_SIZE
    pygame.draw.rect(SCREEN, "YELLOW", (rect_x, rect_y, GRID_SIZE, GRID_SIZE))
    
    red_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    red_surface.fill((255, 0, 0, 100))

    for enemy in storm_troopers + kylo_rens + darth_vaders:
        path = enemy.shortest_path(selected_character, grid)
        for (x, y) in path:
            rect_x = OFFSET_X + x * GRID_SIZE
            rect_y = OFFSET_Y + y * GRID_SIZE
            SCREEN.blit(red_surface, (rect_x, rect_y, GRID_SIZE, GRID_SIZE))

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            value = grid[row][col]

            rect_x = OFFSET_X + col * GRID_SIZE
            rect_y = OFFSET_Y + row * GRID_SIZE

            label = label_positions.get((col, row))
            if label:
                text = font.render(label, True, "WHITE")
                text_rect = text.get_rect(center=(rect_x + GRID_SIZE // 2, rect_y + GRID_SIZE // 2))
                SCREEN.blit(text, text_rect)
            else:
                text = font.render(str(value), True, "BLACK")
                text_rect = text.get_rect(center=(rect_x + GRID_SIZE // 2, rect_y + GRID_SIZE // 2))
                SCREEN.blit(text, text_rect)

    for storm_trooper in storm_troopers:
        SCREEN.blit(STORMTROOPER, (OFFSET_X + storm_trooper.location.char_x * GRID_SIZE, OFFSET_Y + storm_trooper.location.char_y * GRID_SIZE))
    for kylo_ren in kylo_rens:
        SCREEN.blit(KYLO_REN, (OFFSET_X + kylo_ren.location.char_x * GRID_SIZE, OFFSET_Y + kylo_ren.location.char_y * GRID_SIZE))
    for darth_vader in darth_vaders:
        SCREEN.blit(DARTH_VADER, (OFFSET_X + darth_vader.location.char_x * GRID_SIZE, OFFSET_Y + darth_vader.location.char_y * GRID_SIZE))

    if selected_character == master_yoda:
        SCREEN.blit(MASTER_YODA, (OFFSET_X + character.x, OFFSET_Y + character.y))
    elif selected_character == luke_skywalker:
        SCREEN.blit(LUKE_SKYWALKER, (OFFSET_X + character.x, OFFSET_Y + character.y))
    
    SCREEN.blit(TROPHY, (OFFSET_X + GRID_SIZE * GRID_WIDTH - 10, OFFSET_Y + GRID_SIZE * GRID_HEIGHT - 100))
    SCREEN.blit(OK, (OFFSET_X - 60, OFFSET_Y + GRID_SIZE * 5))
    SCREEN.blit(ROTATED_OK_270, (OFFSET_X + GRID_SIZE * 4, OFFSET_Y - 60))
    SCREEN.blit(ROTATED_OK_270, (OFFSET_X + GRID_SIZE * 12, OFFSET_Y - 60))
    SCREEN.blit(ROTATED_OK_90, (OFFSET_X + GRID_SIZE * 4, OFFSET_Y + GRID_SIZE * 10 + 60))
    SCREEN.blit(ROTATED_OK_180, (OFFSET_X + GRID_SIZE * 13 + 60, OFFSET_Y + GRID_SIZE * 5))
    
    font = pygame.font.Font(None, 50)
    text_health = font.render("Health:", True, "BLACK")

    if selected_character == master_yoda and master_yoda.health == 3:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 10 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 14, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 13, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == master_yoda and master_yoda.health == 2.5:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 10 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HALF,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 14, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 13, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == master_yoda and master_yoda.health == 2:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 11 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 14, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == master_yoda and master_yoda.health == 1.5:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 11 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HALF,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 14, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == master_yoda and master_yoda.health == 1:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 12 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == master_yoda and master_yoda.health == 0.5:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 12 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HALF,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
    if selected_character == luke_skywalker and luke_skywalker.health == 3:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 10 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 14, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 13, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == luke_skywalker and luke_skywalker.health == 2:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 11 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 14, OFFSET_Y + GRID_SIZE * 12))
    elif selected_character == luke_skywalker and luke_skywalker.health == 1:
        SCREEN.blit(text_health, (OFFSET_X + GRID_SIZE * 12 + 15, OFFSET_Y + GRID_SIZE * 12 + 5))
        SCREEN.blit(HEART,(OFFSET_X + GRID_SIZE * 15, OFFSET_Y + GRID_SIZE * 12))

    pygame.display.update()

pygame.mixer.init()
pygame.mixer.music.load(music_path)
click = pygame.mixer.Sound(click_sound_path)
effect = pygame.mixer.Sound(effect_sound_path)
victory = pygame.mixer.Sound(victory_sound_path) 

def choose_screen():
    global selected_character
    SCREEN.fill("BLACK")
    MASTER_YODA_RECT = pygame.Rect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 100, 200, 200)
    LUKE_SKYWALKER_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 100, 200, 200)
    MASTER_YODA_CHOOSE = pygame.transform.scale(MASTER_YODA_IMAGE, (200, 200))
    LUKE_SKYWALKER_CHOOSE = pygame.transform.scale(LUKE_SKYWALKER_IMAGE, (200, 200))
    SCREEN.blit(MASTER_YODA_CHOOSE, (MASTER_YODA_RECT.x, MASTER_YODA_RECT.y))
    SCREEN.blit(LUKE_SKYWALKER_CHOOSE, (LUKE_SKYWALKER_RECT.x, LUKE_SKYWALKER_RECT.y))
    font = pygame.font.Font(None, 36)
    text_yoda = font.render("Master Yoda", True, "WHITE")
    text_luke = font.render("Luke Skywalker", True, "WHITE")
    text_prompt = font.render("Please select the character you want to play!", True, "RED")

    SCREEN.blit(LOGO, (SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 - 330))
    SCREEN.blit(text_yoda, (MASTER_YODA_RECT.x + 20, MASTER_YODA_RECT.y - 40))
    SCREEN.blit(text_luke, (LUKE_SKYWALKER_RECT.x + 20, LUKE_SKYWALKER_RECT.y - 40))
    SCREEN.blit(text_prompt, (SCREEN_WIDTH // 2 - 270, SCREEN_HEIGHT // 2 - 50))
    pygame.display.update()
    
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Programı tamamen sonlandır
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(click)
                if MASTER_YODA_RECT.collidepoint(event.pos):
                    selected_character = master_yoda
                    pygame.time.wait(500)
                    running = False  
                elif LUKE_SKYWALKER_RECT.collidepoint(event.pos):
                    selected_character = luke_skywalker
                    pygame.time.wait(500)
                    running = False
        pygame.display.update()

    pygame.mixer.music.stop()

enemies = storm_troopers + kylo_rens + darth_vaders

def check_and_reset(selected_character, enemies, grid, original_grid):
    for enemy in enemies:
        if (selected_character.location.char_x == enemy.location.char_x and 
            selected_character.location.char_y == enemy.location.char_y):
            
            if isinstance(selected_character, MasterYoda):
                selected_character.decrease_health()

            elif isinstance(selected_character, LukeSkywalker):
                selected_character.decrease_health()

            pygame.mixer.Sound.play(effect)
            pygame.time.wait(1000)
            pygame.event.clear()

            # Reset the grid
            grid[:] = [row[:] for row in original_grid]

            for i, storm_trooper in enumerate(storm_troopers):
                start_position = stormtrooper_start_positions[i]
                storm_trooper.location.char_x, storm_trooper.location.char_y = start_position
            
            for i, kylo_ren in enumerate(kylo_rens):
                start_position = kyloren_start_positions[i]
                kylo_ren.location.char_x, kylo_ren.location.char_y = start_position

            for i, darth_vader in enumerate(darth_vaders):
                start_position = darth_vader_start_positions[i]
                darth_vader.location.char_x, darth_vader.location.char_y = start_position

            if isinstance(selected_character, MasterYoda):
                selected_character.location.char_x = master_yoda_start_char_x
                selected_character.location.char_y = master_yoda_start_char_y
            elif isinstance(selected_character, LukeSkywalker):
                selected_character.location.char_x = luke_skywalker_start_char_x
                selected_character.location.char_y = luke_skywalker_start_char_y

            return True
    return False

def reset_game():
    global selected_character, grid, original_grid, master_yoda, luke_skywalker

    grid = [row[:] for row in original_grid]

    master_yoda.location.char_x = master_yoda_start_char_x
    master_yoda.location.char_y = master_yoda_start_char_y
    master_yoda.set_health(3)

    luke_skywalker.location.char_x = luke_skywalker_start_char_x
    luke_skywalker.location.char_y = luke_skywalker_start_char_y
    luke_skywalker.set_health(3)

    for i, storm_trooper in enumerate(storm_troopers):
        start_position = stormtrooper_start_positions[i]
        storm_trooper.location.char_x, storm_trooper.location.char_y = start_position

    for i, kylo_ren in enumerate(kylo_rens):
        start_position = kyloren_start_positions[i]
        kylo_ren.location.char_x, kylo_ren.location.char_y = start_position

    for i, darth_vader in enumerate(darth_vaders):
        start_position = darth_vader_start_positions[i]
        darth_vader.location.char_x, darth_vader.location.char_y = start_position

    choose_screen()

def game_over_screen():
    SCREEN.fill("BLACK")
    font = pygame.font.Font(None, 100)
    text = font.render("GAME OVER", True, "RED")
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.update()

    pygame.time.wait(3000)
    reset_game()

winning_position = (13, 9)

def game_won_screen():
    SCREEN.fill("BLACK")
    font = pygame.font.Font(None, 100)
    text = font.render("YOU WON THE GAME!", True, "GREEN")
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.update()
    pygame.mixer.Sound.play(victory)
    pygame.time.wait(4300) 
    reset_game()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    global selected_character
    global grid
    selected_character = None
    choose_screen()

    player_made_move = False
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if selected_character == master_yoda:
                    if event.key == pygame.K_LEFT:
                        selected_character.move("left", grid)
                        player_made_move = True
                    elif event.key == pygame.K_RIGHT:
                        selected_character.move("right", grid)
                        player_made_move = True
                    elif event.key == pygame.K_UP:
                        selected_character.move("up", grid)
                        player_made_move = True
                    elif event.key == pygame.K_DOWN:
                        selected_character.move("down", grid)
                        player_made_move = True
                elif selected_character == luke_skywalker:
                    if event.key == pygame.K_LEFT:
                        selected_character.move("left", grid)
                        player_made_move = True
                    elif event.key == pygame.K_RIGHT:
                        selected_character.move("right", grid)
                        player_made_move = True
                    elif event.key == pygame.K_UP:
                        selected_character.move("up", grid)
                        player_made_move = True
                    elif event.key == pygame.K_DOWN:
                        selected_character.move("down", grid)
                        player_made_move = True

        if (selected_character.location.get_x(), selected_character.location.get_y()) == winning_position:
            game_won_screen()

        if check_and_reset(selected_character, enemies, grid, original_grid):
            if selected_character.get_health() <= 0:
                game_over_screen()
            player_made_move = False
            continue

        if player_made_move:

            for storm_trooper in storm_troopers:
                path = storm_trooper.shortest_path(selected_character, grid)
                if path and len(path) > 1:
                    storm_trooper.location.char_x, storm_trooper.location.char_y = path[1]

            for kylo_ren in kylo_rens:
                path = kylo_ren.shortest_path(selected_character, grid)
                if path and len(path) > 2:
                    kylo_ren.location.char_x, kylo_ren.location.char_y = path[2]
                elif path and len(path) > 1:
                    kylo_ren.location.char_x, kylo_ren.location.char_y = path[1]

            for darth_vader in darth_vaders:
                path = darth_vader.shortest_path(selected_character, grid)
                if path and len(path) > 1:
                    darth_vader.location.char_x, darth_vader.location.char_y = path[1]
                    current_x, current_y = darth_vader.location.char_x, darth_vader.location.char_y
                    if grid[current_y][current_x] == 0:
                        grid[current_y][current_x] = 1 

            player_made_move = False 

        character = pygame.Rect(selected_character.location.char_x * GRID_SIZE, selected_character.location.char_y * GRID_SIZE, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        draw_screen(character)
main()