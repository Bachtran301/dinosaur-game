import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_0 = pygame.image.load('graphics/player/0.png').convert_alpha()
		player_walk_1 = pygame.image.load('graphics/player/1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/2.png').convert_alpha()
		player_walk_3 = pygame.image.load('graphics/player/3.png').convert_alpha()
		player_walk_4 = pygame.image.load('graphics/player/4.png').convert_alpha()
		player_walk_5 = pygame.image.load('graphics/player/5.png').convert_alpha()
		player_walk_6 = pygame.image.load('graphics/player/6.png').convert_alpha()
		player_walk_7 = pygame.image.load('graphics/player/7.png').convert_alpha()

  
  
		player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		# Phóng to và đặt màu trong suốt cho hình ảnh
		self.player_walk = [
			pygame.transform.scale(player_walk_0, (player_walk_0.get_width() * 3.5, player_walk_0.get_height() * 3.5)),
            pygame.transform.scale(player_walk_1, (player_walk_1.get_width() * 3.5, player_walk_1.get_height() * 3.5)),
            pygame.transform.scale(player_walk_2, (player_walk_2.get_width() * 3.5, player_walk_2.get_height() * 3.5)),
            pygame.transform.scale(player_walk_3, (player_walk_3.get_width() * 3.5, player_walk_3.get_height() * 3.5)),
            pygame.transform.scale(player_walk_4, (player_walk_4.get_width() * 3.5, player_walk_4.get_height() * 3.5)),
            pygame.transform.scale(player_walk_5, (player_walk_5.get_width() * 3.5, player_walk_5.get_height() * 3.5)),
            pygame.transform.scale(player_walk_6, (player_walk_6.get_width() * 3.5, player_walk_6.get_height() * 3.5)),
            pygame.transform.scale(player_walk_7, (player_walk_7.get_width() * 3.5, player_walk_7.get_height() * 3.5)),
            
            
		]
		for i in range(len(self.player_walk)):
			self.player_walk[i].set_colorkey((0, 0, 0))

		self.player_jump = pygame.transform.scale(player_jump, (player_jump.get_width() * 3.5, player_jump.get_height() * 3.5))
		self.player_jump.set_colorkey((0, 0, 0))

		self.player_index = 0

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			#self.jump_sound.play()

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
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
   
			self.frames = [
       			pygame.transform.scale(fly_1, (fly_1.get_width() * 0.8, fly_1.get_height() * 0.8)),
    			pygame.transform.scale(fly_2, (fly_2.get_width() * 0.8, fly_2.get_height() * 0.8)),
			]
			y_pos = 210
		elif type == 'ufo':
			ufo = pygame.image.load('graphics/ufo/ufo.png').convert_alpha()
			
			self.frames = [
				pygame.transform.scale(ufo, (ufo.get_width() * 0.65, ufo.get_height() * 0.65)),
			]
			y_pos = 210
		elif type == 'snail':
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
   
			self.frames = [
            	pygame.transform.scale(snail_1, (snail_1.get_width() * 1, snail_1.get_height() * 1)),
            	pygame.transform.scale(snail_2, (snail_2.get_width() * 1, snail_2.get_height() * 1)),
        	]
			#self.frames = [snail_1,snail_2]
			y_pos  = 300
		elif type == 'cactus':
			cactus = pygame.image.load('graphics/cactus/cactus.png').convert_alpha()
			
			self.frames = [
				pygame.transform.scale(cactus, (cactus.get_width() * 1, cactus.get_height() * 1)),
			]
			y_pos = 300

		elif type == 'zombie':
			FlagZombie_0 = pygame.image.load('graphics/zombie/FlagZombie_0.png').convert_alpha()
			FlagZombie_1 = pygame.image.load('graphics/zombie/FlagZombie_1.png').convert_alpha()
			FlagZombie_2 = pygame.image.load('graphics/zombie/FlagZombie_2.png').convert_alpha()
			FlagZombie_3 = pygame.image.load('graphics/zombie/FlagZombie_3.png').convert_alpha()
			FlagZombie_4 = pygame.image.load('graphics/zombie/FlagZombie_4.png').convert_alpha()
			FlagZombie_5 = pygame.image.load('graphics/zombie/FlagZombie_5.png').convert_alpha()
			FlagZombie_6 = pygame.image.load('graphics/zombie/FlagZombie_6.png').convert_alpha()
			FlagZombie_7 = pygame.image.load('graphics/zombie/FlagZombie_7.png').convert_alpha()
			FlagZombie_8 = pygame.image.load('graphics/zombie/FlagZombie_8.png').convert_alpha()
			FlagZombie_9 = pygame.image.load('graphics/zombie/FlagZombie_9.png').convert_alpha()
			FlagZombie_10 = pygame.image.load('graphics/zombie/FlagZombie_10.png').convert_alpha()
			FlagZombie_11 = pygame.image.load('graphics/zombie/FlagZombie_11.png').convert_alpha()
			self.frames = [
       			pygame.transform.scale(FlagZombie_0, (FlagZombie_0.get_width() * 0.57, FlagZombie_0.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_1, (FlagZombie_1.get_width() * 0.57, FlagZombie_1.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_2, (FlagZombie_2.get_width() * 0.57, FlagZombie_2.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_3, (FlagZombie_3.get_width() * 0.57, FlagZombie_3.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_4, (FlagZombie_4.get_width() * 0.57, FlagZombie_4.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_5, (FlagZombie_5.get_width() * 0.57, FlagZombie_5.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_6, (FlagZombie_6.get_width() * 0.57, FlagZombie_6.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_7, (FlagZombie_7.get_width() * 0.57, FlagZombie_7.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_8, (FlagZombie_8.get_width() * 0.57, FlagZombie_8.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_9, (FlagZombie_9.get_width() * 0.57, FlagZombie_9.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_10, (FlagZombie_10.get_width() * 0.57, FlagZombie_10.get_height() * 0.57)),
    			pygame.transform.scale(FlagZombie_11, (FlagZombie_11.get_width() * 0.57, FlagZombie_11.get_height() * 0.57)),
			]
			y_pos = 301
		

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def display_high_score(high_score):
    high_score_surf = test_font.render(f'High Score: {high_score}', False, (255, 255, 255))
    high_score_rect = high_score_surf.get_rect(center=(600, 50))
    screen.blit(high_score_surf, high_score_rect)



def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Ninja Jumper')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
game_speed = 6
high_score = 0
#bg_music = pygame.mixer.Sound('audio/music.wav')
#bg_music.play(loops = -1)



#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface_1 = pygame.image.load('graphics/Sky1.png').convert()
sky_surface_2 = pygame.image.load('graphics/Sky2.png').convert()
sky_surface_3 = pygame.image.load('graphics/Sky3.png').convert()
sky_surface_4 = pygame.image.load('graphics/Sky4.png').convert()


#sky_surface = pygame.image.load('graphics/background.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,5) # Phóng to hình ảnh
player_stand.set_colorkey((0, 0, 0)) # Đặt màu trong suốt
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# Load high score từ file


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail','ufo','zombie','cactus'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)
				score = 0

	if game_active:
		# Change the background based on the score
		if score < 20:
			screen.blit(sky_surface_1, (0,0))
		elif score < 35:
			screen.blit(sky_surface_2, (0,0))
		elif score < 50:
			screen.blit(sky_surface_3, (0,0))
		else:
			screen.blit(sky_surface_4, (0,0))
		
		screen.blit(ground_surface, (0,300))
		score = display_score()

		# Adjust the speed based on the score
		if score < 10:
			game_speed = 6
		elif score < 20:
			game_speed = 8
		else:
			game_speed = 10
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		display_high_score(high_score)
		
	else:
		if score > high_score:
			high_score = score
   
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else:
			screen.blit(score_message,score_message_rect)
			#display_high_score(high_score)

	pygame.display.update()
	clock.tick(60)
 