import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60
run = True
start_screen = True
screen_width = 864
screen_height = 936
game_over = False
start_game = False
scroll_speed = 4
platform_frquency = 750
last_platform = pygame.time.get_ticks() - platform_frquency
gravity = 1
randInt1 = random.randint(0, int(screen_width))
randInt2 = random.randint(0, int(screen_width))
randInt3 = random.randint(0, int(screen_width)) 
score = 0  
best_score = 0 

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

# Player movement variables
player_speed = 7  # Horizontal movement speed
player_width = 50
player_height = 75

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump Game")

# Define background color (RGB)
background_color = (255, 204, 153)  # cream

#render text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#rest game funct
def rest_game():
    Platform_group.empty()
    Coin_group.empty()
    player.rect.x = int(screen_width / 2) - 35
    player.rect.y = 506
    score = 0

    #Adding coin sprites
    coin1 = Coin(randInt2, 366)
    coin2 = Coin(randInt3, 166)
    Coin_group.add(coin1)
    Coin_group.add(coin2)

    #Adding platform sprites
    platform1 = Platform(int(screen_width / 2), 606, 100, 20)
    platform2 = Platform(randInt2, 406, 100, 20)
    platform3 = Platform(randInt3, 206, 100, 20)
    Platform_group.add(platform1)
    Platform_group.add(platform2)
    Platform_group.add(platform3)
    return score


#create class for player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.vel_y = 0  # Vertical velocity
        self.jump_strength = -30  # Negative value for upward movement
        self.on_ground = False  # Indicates if the player is on a platform or ground
        self.vel_x = 0  # Horizontal velocity
        self.y = y

        for num in range(1, 3):
           img = pygame.image.load(f'player{num}.png')
           self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        #animation
        self.counter += 1
        cooldown = 50
        if self.counter > cooldown:
           self.counter = 0
           self.index += 1
           if self.index >= len(self.images):
              self.index = 0
        self.image = self.images[self.index]

        # Handle horizontal movement
        keys = pygame.key.get_pressed()
        self.vel_x = 0  # Reset horizontal velocity each frame

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = player_speed

        self.rect.x += self.vel_x

        # Keep player within screen bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        # Handle jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Apply gravity
        self.vel_y += gravity
        self.rect.y += int(self.vel_y)

        # Collision detection with platforms
        self.on_ground = False  # Reset on_ground before checking collisions
        platform_collisions = pygame.sprite.spritecollide(self, Platform_group, False)
        for platform in platform_collisions:
            # Check if player is falling
            if self.vel_y > 0:
                # Check if player's bottom is above the platform's top before moving
                if self.rect.bottom - self.vel_y <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Prevent the player from falling below the screen
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.vel_y = 0
            self.on_ground = True

Player_group = pygame.sprite.Group()
player = Player(int(screen_width / 2), 550)
Player_group.add(player)

#platform sprite
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('platform.png')
        self.image = pygame.transform.scale(self.image, (width * 2, height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] 

    def update(self):
        self.rect.y += scroll_speed
        if self.rect.top >= screen_height:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += scroll_speed
        if self.rect.top >= screen_height:
            self.kill()

class button():
    def __init__(self, x, y):
        self.image = pygame.image.load('restart.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        #mose pos
        pos = pygame.mouse.get_pos()

        #check if mouse over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


#Adding coin sprites
Coin_group = pygame.sprite.Group()
coin1 = Coin(randInt2, 366)
coin2 = Coin(randInt3, 166)
Coin_group.add(coin1)
Coin_group.add(coin2)

#Adding platform sprites
Platform_group = pygame.sprite.Group()
platform1 = Platform(int(screen_width / 2), 606, 100, 20)
platform2 = Platform(randInt2, 406, 100, 20)
platform3 = Platform(randInt3, 206, 100, 20)
Platform_group.add(platform1)
Platform_group.add(platform2)
Platform_group.add(platform3)


#restart instance
button = button(screen_width / 2 - 110, screen_height / 2 - 100)

#start screen
while start_screen:
    #update background
    screen.fill(background_color)
    draw_text("JUMP GAME", font, white, int(screen_width / 2) - 120, 20)
    draw_text("CLICK TO START GAME", font, white, int(screen_width / 2) - 240, 70)


    #proceed to game
    if pygame.mouse.get_pressed()[0] == 1:
            start_screen = False

    #event handler
    for event in pygame.event.get():
        #quit program
        if event.type == pygame.QUIT:
            run = False
            start_screen = False

    #update display
    pygame.display.flip()

#game loop
while run:

    clock.tick(fps)

    #update background
    screen.fill(background_color)

    #draw opening game screen sprites
    Player_group.draw(screen)
    Platform_group.draw(screen)  
    Coin_group.draw(screen)

    #coin collect
    if pygame.sprite.groupcollide(Player_group, Coin_group, False, True):
        score += 1

    #start game 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
            start_game = True

    #collision loop
    if start_game == True and game_over == False:
        #generate platform
        time_now = pygame.time.get_ticks()
        if time_now - last_platform > platform_frquency:
            randInt = random.randint(0, int(screen_width))
            platform = Platform(randInt, 40, 100, 20)
            Platform_group.add(platform)
            coin = Coin(randInt, 0)
            Coin_group.add(coin)
            last_platform = time_now

        Player_group.update()
        Platform_group.update()
        Coin_group.update()


    if score > best_score:
        best_score = score
    
    draw_text(f"Score: {score}", font, white, screen_width - 200, 20)
    draw_text(f"Best Score:{best_score}", font, white, 10, 20)


    if player.rect.bottom >= screen_height:
        game_over = True

    #check for game over
    if game_over == True:
        if button.draw() == True:
            game_over = False
            start_game = False
            score = 0
            rest_game()

    #event handler
    for event in pygame.event.get():
        #quit program
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()

pygame.quit()
 