import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.character = character
        if character == 'Ninja':
            self.load_Ninja()
        elif character == 'Rabbiter':
            self.load_Rabbiter()
        elif character == 'Villager':
            self.load_Villager()

        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        # self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        # self.jump_sound.set_volume(0.5)

    def load_Ninja(self):
        self.player_walk = [self.load_and_scale(f'graphics/player/Ninja/{i}.png', 3) for i in range(8)]
        self.player_jump = self.load_and_scale('graphics/player/Ninja/jump.png', 3)

    def load_Rabbiter(self):
        self.player_walk = [self.load_and_scale(f'graphics/player/Rabbiter/{i}.png', 1) for i in range(3)]
        self.player_jump = self.load_and_scale('graphics/player/Rabbiter/jump.png', 1)

    def load_Villager(self):
        self.player_walk = [self.load_and_scale(f'graphics/player/Villager/{i}.png', 3) for i in range(8)]
        self.player_jump = self.load_and_scale('graphics/player/Villager/jump.png', 3)

    def load_and_scale(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        img.set_colorkey((0, 0, 0))
        return img

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            # self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        y_pos = 300
        if type == 'fly':
            self.frames = [self.load_and_scale(f'graphics/fly/fly{i}.png', 0.75) for i in range(2)]
            y_pos = 210
        elif type == 'bee':
            self.frames = [self.load_and_scale(f'graphics/bee/bee{i}.png', 0.75) for i in range(2)]
            y_pos = 210
        elif type == 'snail':
            self.frames = [self.load_and_scale(f'graphics/snail/snail{i}.png', 1) for i in range(2)]
        elif type == 'cactus':
            self.frames = [self.load_and_scale('graphics/cactus/cactus.png', 1)]
        elif type == 'worm':
            self.frames = [self.load_and_scale(f'graphics/worm/worm{i}.png', 1) for i in range(2)]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def load_and_scale(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        return img

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/coin/gold.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), randint(150, 250)))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def display_high_score(high_score):
    high_score_surf = test_font.render(f'High Score: {high_score}', False, (255, 255, 255))
    high_score_rect = high_score_surf.get_rect(center=(600, 50))
    screen.blit(high_score_surf, high_score_rect)

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

def collision_coin():
    global start_time
    if pygame.sprite.spritecollide(player.sprite, coin_group, True):
        start_time -= 5  # Subtract 5 seconds to add to the score

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
game_speed = 6
high_score = 0
player_choice = None

# Load all player stand images for selection
player_stand_images = [
    ('Ninja', pygame.image.load('graphics/player/Ninja/player_stand.png').convert_alpha(), (200, 200), 5),
    ('Rabbiter', pygame.image.load('graphics/player/Rabbiter/player_stand.png').convert_alpha(), (400, 200), 1.3),
    ('Villager', pygame.image.load('graphics/player/Villager/player_stand.png').convert_alpha(), (600, 200), 5),
]

for i in range(len(player_stand_images)):
    player_stand_images[i] = (
        player_stand_images[i][0],
        pygame.transform.rotozoom(player_stand_images[i][1], 0, player_stand_images[i][3]),
        player_stand_images[i][2],
    )
    player_stand_images[i][1].set_colorkey((0, 0, 0))

# Groups
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

sky_surfaces = [
    pygame.image.load(f'graphics/Sky{i}.png').convert() for i in range(1, 5)
]
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
game_name = test_font.render('Select character', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 375))

# Timer
obstacle_timer = pygame.USEREVENT + 1
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer, 1500)
pygame.time.set_timer(coin_timer, 5000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'cactus', 'snail', 'bee', 'worm', 'cactus'])))
            if event.type == coin_timer:
                coin_group.add(Coin())
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.rect.collidepoint(event.pos) and player.rect.bottom >= 300:
                    player.gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.rect.bottom >= 300:
                    player.sprite.gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_choice:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    player.add(Player(player_choice))

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, img, pos in player_stand_images:
                    if img.get_rect(center=pos).collidepoint(event.pos):
                        player_choice = name

    if game_active:
        screen.blit(sky_surfaces[min(score // 20, 3)], (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        coin_group.draw(screen)
        coin_group.update()

        game_active = collision_sprite()
        collision_coin()
        display_high_score(high_score)
        
        
    else:
        if score > high_score:
            high_score = score

        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        for _, img, pos in player_stand_images:
            screen.blit(img, img.get_rect(center=pos))

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 120))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        if player_choice:
            selected_surf = test_font.render(f'Selected: {player_choice}', False, (111, 196, 169))
            selected_rect = selected_surf.get_rect(center=(400, 300))
            screen.blit(selected_surf, selected_rect)

    pygame.display.update()
    clock.tick(60)
