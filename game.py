import pygame
from sys import exit
from random import randint, choice
import random
import os
from app.utils import submit_score, get_high_scores
import pyperclip

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

# Game states
INITIAL_MENU = "initial_menu"
NAME_INPUT = "name_input"
CHARACTER_SELECTION = "character_selection"
GAME_PLAYING = "game_playing"
RANKINGS_DISPLAY = "rankings_display"
LINK_DISPLAY = "link_display"
game_state = INITIAL_MENU

# Game variables
game_active = False
start_time = 0
score = 0
game_speed = 6
high_score = 0
player_choice = None
selection_message = ""
rankings = []
player_name = ""
name_input_active = False
link_to_display = "https://dinosaur-game.onrender.com/"
link_copied = False

# Load images
sky_surfaces = [pygame.image.load(f'graphics/Sky{i}.png').convert() for i in range(1, 5)]
ground_surface = pygame.image.load('graphics/ground.png').convert()
start_image = pygame.image.load('graphics/start_btn.png').convert_alpha()
exit_image = pygame.image.load('graphics/exit_btn.png').convert_alpha()
start_image_rect = start_image.get_rect(center=(200, 200))
exit_image_rect = exit_image.get_rect(center=(600, 200))

# Load player stand images for selection
player_stand_images = [
    ('Ninja', pygame.image.load('graphics/player/Ninja/player_stand.png').convert_alpha(), (200, 200), 5, 0),
    ('Rabbiter', pygame.image.load('graphics/player/Rabbiter/player_stand.png').convert_alpha(), (400, 200), 1.3, 10),
    ('Villager', pygame.image.load('graphics/player/Villager/player_stand.png').convert_alpha(), (600, 200), 0.8, 20),
]

for i in range(len(player_stand_images)):
    player_stand_images[i] = (
        player_stand_images[i][0],
        pygame.transform.rotozoom(player_stand_images[i][1], 0, player_stand_images[i][3]),
        player_stand_images[i][2],
        player_stand_images[i][4]
    )
    player_stand_images[i][1].set_colorkey((0, 0, 0))

# Intro screen
game_name = test_font.render('Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 380))

# Groups
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 5000)
min_obstacle_timer = 800
max_obstacle_timer = 1500

# Load high scores
high_scores = get_high_scores()

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

    def load_Ninja(self):
        self.player_walk = [self.load_and_scale(f'graphics/player/Ninja/{i}.png', 3) for i in range(8)]
        self.player_jump = self.load_and_scale('graphics/player/Ninja/jump.png', 3)
        self.load_jump_sound()

    def load_Rabbiter(self):
        self.player_walk = [self.load_and_scale(f'graphics/player/Rabbiter/{i}.png', 1) for i in range(3)]
        self.player_jump = self.load_and_scale('graphics/player/Rabbiter/jump.png', 1)
        self.load_jump_sound()
        
    def load_Villager(self):
        self.player_walk = [self.load_and_scale(f'graphics/player/Villager/{i}.png', 0.5) for i in range(4)]
        self.player_jump = self.load_and_scale('graphics/player/Villager/jump.png', 0.5)
        self.load_jump_sound()
        
    def load_jump_sound(self):
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)
    
    def load_and_scale(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        img.set_colorkey((0, 0, 0))
        return img

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

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
        self.type = type
        y_pos = 300
        if type == 'fly':
            self.frames = [self.load_and_scale(f'graphics/fly/fly{i}.png', 0.75) for i in range(2)]
            y_pos = 210
        elif type == 'spikes':
            self.frames = [self.load_and_scale(f'graphics/spikes/spikes{i}.png', 0.75) for i in range(1)]
        elif type == 'snail':
            self.frames = [self.load_and_scale(f'graphics/snail/snail{i}.png', 1) for i in range(2)]
        elif type == 'tooth':
            self.frames = [self.load_and_scale('graphics/tooth/tooth.png', 1)]
        elif type == 'bee':
            self.frames = [self.load_and_scale(f'graphics/bee/bee{i}.png', 0.75) for i in range(2)]
            y_pos = 210
        elif type == 'worm':
            self.frames = [self.load_and_scale(f'graphics/worm/worm{i}.png', 1) for i in range(2)]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def load_and_scale(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        img.set_colorkey((0, 0, 0))
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
    def __init__(self, coin_type):
        super().__init__()
        self.coin_type = coin_type
        if coin_type == 'gold':
            self.image = pygame.image.load('graphics/coin/gold.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
            self.rect = self.image.get_rect(midbottom=(randint(900, 1100), randint(150, 250)))
        elif coin_type == 'diamond':
            self.image = pygame.image.load('graphics/coin/diamond.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
            self.rect = self.image.get_rect(midbottom=(randint(900, 1100), randint(100, 150)))

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

def display_rankings(rankings):
    rankings_surf = test_font.render('Rankings:', False, (255, 255, 255))
    rankings_rect = rankings_surf.get_rect(center=(400, 50))
    screen.blit(rankings_surf, rankings_rect)
    
    columns = [('Rank', 200), ('Name', 400), ('Score', 600)]
    for title, x in columns:
        surf = test_font.render(title, False, (255, 255, 255))
        rect = surf.get_rect(center=(x, 100))
        screen.blit(surf, rect)
    
    for i, score in enumerate(rankings[:5]):
        rank_surf = test_font.render(f'{i + 1}', False, (255, 255, 255))
        rank_rect = rank_surf.get_rect(center=(200, 150 + i * 50))
        screen.blit(rank_surf, rank_rect)
        
        name_surf = test_font.render(score['player_name'], False, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(400, 150 + i * 50))
        screen.blit(name_surf, name_rect)
        
        score_surf = test_font.render(f'{score["score"]}', False, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(600, 150 + i * 50))
        screen.blit(score_surf, score_rect)

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

def collision_coin():
    global start_time
    if pygame.sprite.spritecollide(player.sprite, coin_group, True):
        start_time -= 2  # cộng điểm khi nhặt coin

def save_high_scores(scores, filename='high_scores.txt'):
    with open(filename, 'w') as file:
        for score in scores:
            file.write(f"{score}\n")

def load_high_scores(filename='high_scores.txt'):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        high_scores = []
        for line in file:
            try:
                score_data = eval(line.strip())
                if isinstance(score_data, dict) and 'player_name' in score_data and 'score' in score_data:
                    high_scores.append(score_data)
                elif isinstance(score_data, int):
                    high_scores.append({"player_name": "Unknown", "score": score_data})
            except:
                print(f"Invalid line in high scores file: {line}")
        return high_scores

def add_score_to_rankings(new_score, filename='high_scores.txt'):
    high_scores = load_high_scores(filename)
    
    # Thêm điểm số mới
    high_scores.append(new_score)
    
    # Sắp xếp theo điểm số giảm dần
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)
    
    # Loại bỏ các bản ghi trùng lặp, giữ lại bản ghi đầu tiên (điểm cao nhất) cho mỗi người chơi
    seen_players = set()
    unique_scores = []
    for score in high_scores:
        if score['player_name'] not in seen_players:
            unique_scores.append(score)
            seen_players.add(score['player_name'])
    
    # Giữ lại top 5 điểm cao nhất
    high_scores = unique_scores[:5]
    
    # Lưu điểm cao mới
    save_high_scores(high_scores, filename)
    
    return high_scores
    
def handle_name_input(event):
    global player_name, game_state, name_input_active
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if player_name:
                game_state = CHARACTER_SELECTION
                name_input_active = False
        elif event.key == pygame.K_BACKSPACE:
            player_name = player_name[:-1]
        else:
            if len(player_name) < 10 and event.unicode.isprintable():  # Giới hạn độ dài tên và chỉ cho phép ký tự in được
                player_name += event.unicode

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_scores(high_scores)
            pygame.quit()
            exit()
        
        if game_state == INITIAL_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_state = NAME_INPUT
                elif event.key == pygame.K_e:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_image_rect.collidepoint(event.pos):
                    game_state = NAME_INPUT
                elif exit_image_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        elif game_state == NAME_INPUT:
            handle_name_input(event)
        elif game_state == CHARACTER_SELECTION:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_choice:
                    game_state = GAME_PLAYING
                    start_time = int(pygame.time.get_ticks() / 1000)
                    player.add(Player(player_choice))
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, img, pos, required_score in player_stand_images:
                    if img.get_rect(center=pos).collidepoint(event.pos):
                        if high_score >= required_score:
                            player_choice = name
                            selection_message = ""
                        else:
                            selection_message = f"{name} requires {required_score} points!"
        elif game_state == GAME_PLAYING:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'spikes', 'snail', 'bee', 'worm', 'tooth'])))
                new_timer = max(min_obstacle_timer, max_obstacle_timer - (score * 15))
                pygame.time.set_timer(obstacle_timer, new_timer)
            if event.type == coin_timer:
                if random.random() < 0.05:
                    coin_group.add(Coin('diamond'))
                else:
                    coin_group.add(Coin('gold'))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.sprite.rect.collidepoint(event.pos) and player.sprite.rect.bottom >= 300:
                    player.sprite.gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.rect.bottom >= 300:
                    player.sprite.gravity = -20
        elif game_state == RANKINGS_DISPLAY:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = LINK_DISPLAY
                link_copied = False
        elif game_state == LINK_DISPLAY:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = CHARACTER_SELECTION
                link_copied = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if actual_link_rect.collidepoint(mouse_pos):
                    pyperclip.copy(link_to_display)
                    link_copied = True
                

    if game_state == INITIAL_MENU:
        screen.fill((94, 129, 162))
        screen.blit(start_image, start_image_rect)
        screen.blit(exit_image, exit_image_rect)
    elif game_state == NAME_INPUT:
        screen.fill((94, 129, 162))
        name_prompt = test_font.render('Enter your name: ', False, (255, 255, 255))
        name_surface = test_font.render(player_name, False, (255, 255, 255))
    
        prompt_width = name_prompt.get_width()
        total_width = prompt_width + name_surface.get_width()
        start_x = (800 - total_width) // 2  # Căn giữa theo chiều ngang
    
        screen.blit(name_prompt, (start_x, 150))
        screen.blit(name_surface, (start_x + prompt_width, 150))
    
        if pygame.time.get_ticks() % 1000 < 500:  # Nhấp nháy con trỏ
            cursor_x = start_x + prompt_width + name_surface.get_width()
            pygame.draw.line(screen, (255, 255, 255), (cursor_x, 150), (cursor_x, 175), 2)
    elif game_state == CHARACTER_SELECTION:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        for _, img, pos, _ in player_stand_images:
            screen.blit(img, img.get_rect(center=pos))

        score_message = test_font.render(f'High score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 120))
        screen.blit(score_message, score_message_rect)

        if player_choice and selection_message == "":
            selected_surf = test_font.render(f'Selected: {player_choice}', False, (111, 196, 169))
            selected_rect = selected_surf.get_rect(center=(400, 300))
            screen.blit(selected_surf, selected_rect)

        if selection_message:
            message_surf = test_font.render(selection_message, False, (255, 0, 0))
            message_rect = message_surf.get_rect(center=(400, 320))
            screen.blit(message_surf, message_rect)
    elif game_state == GAME_PLAYING:
        screen.blit(sky_surfaces[min(score // 10, 3)], (0, 0))
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
        
        if not game_active:
            game_state = RANKINGS_DISPLAY
            new_score = {"player_name": player_name, "score": score}
            rankings = [{"player_name": "Unknown", "score": s} if isinstance(s, int) else s for s in rankings]
            rankings.append(new_score)
            rankings.sort(key=lambda x: x["score"], reverse=True)
            if len(rankings) > 5:
                rankings = rankings[:5]
            submit_score(player_name, score)
            high_scores = get_high_scores()
            rankings = high_scores
            high_score = max(high_score, score)
    elif game_state == RANKINGS_DISPLAY:
        screen.fill((94, 129, 162))
        add_score_to_rankings({"player_name": player_name, "score": score})
        high_scores = get_high_scores()
        display_high_score(max(score['score'] for score in high_scores) if high_scores else 0)
        display_rankings(high_scores)
    elif game_state == LINK_DISPLAY:
        screen.fill((94, 129, 162))
        link_surf = test_font.render('Check out the top score leaderboard:', False, (255, 255, 255))
        link_rect = link_surf.get_rect(center=(400, 150))
        screen.blit(link_surf, link_rect)

        actual_link_surf = test_font.render(link_to_display, False, (111, 196, 169))
        actual_link_rect = actual_link_surf.get_rect(center=(400, 200))
        screen.blit(actual_link_surf, actual_link_rect)

        # Vẽ khung viền
        pygame.draw.rect(screen, (111, 196, 169), actual_link_rect.inflate(10, 10), 2)

        if link_copied:
            copy_surf = test_font.render('Link copied!', False, (0, 255, 0))
        else:
            copy_surf = test_font.render('Click to copy link', False, (255, 255, 255))
        copy_rect = copy_surf.get_rect(center=(400, 250))
        screen.blit(copy_surf, copy_rect)

        continue_surf = test_font.render('Press SPACE to continue', False, (255, 255, 255))
        continue_rect = continue_surf.get_rect(center=(400, 300))
        screen.blit(continue_surf, continue_rect)

    pygame.display.update()
    clock.tick(60)
    #hello world 123