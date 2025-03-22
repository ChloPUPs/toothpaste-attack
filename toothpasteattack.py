import pygame
import sys
import random

pygame.init()

# Sounds
pygame.mixer.init()
ToothpasteAppearSFX = pygame.mixer.Sound("ToothpasteAppearSFX.mp3")
PlayerDeathSFX = pygame.mixer.Sound("PlayerDeathSFX.mp3")

# Music
pygame.mixer.music.load("Music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Channels
channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)

# Variables
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

timer = 0

score = 0

font = pygame.font.Font("freesansbold.ttf", 20)

# Background
background = pygame.image.load("Background.png")

# Classes
class Player:
    def __init__(self, startX, startY):
        self.startX = startX
        self.startY = startY
        self.velocity = [0, 0]
        self.movement = [False, False, False, False]
        self.img = pygame.image.load("player.png")
        self.rect = pygame.Rect(startX, startY, self.img.get_width(), self.img.get_height())

class Enemy:
    def __init__(self, velocity):
        self.velocity = velocity
        self.img = pygame.image.load("toothpaste.png")
        self.rect = pygame.Rect(random.randrange(0, screen.get_width() + 1), self.img.get_height() * -1, self.img.get_width(), self.img.get_height())

# movement[0] = left, movement[1] = right, movement[2] = up, movement[3] = down.

# Initial things
player = Player(320, 360)

# Enemies
enemies = []
# Summon 10 enemies
for i in range(10):
    # Add the enemy to enemies list
    enemies.append(Enemy(-3 - i))

def resetTOOTHPast():
    global enemies
    for i in enemies:
        i.rect.x = random.randrange(0, screen.get_width() + 1)
        i.rect.y = i.img.get_height() * -1

# Game over
game_over_img = pygame.image.load("gameovertext.png")
is_game_over = False

def show_text(score):
    rendered_score = font.render("Toothpaste dodged: " + score, True, (0, 0, 0))
    screen.blit(rendered_score, (20, 20))

# Game loop
while True:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.movement[0] = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.movement[1] = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.movement[2] = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:                
                player.movement[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.movement[0] = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.movement[1] = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.movement[2] = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.movement[3] = False

    # Background
    screen.fill((0, 200, 255))
    screen.blit(background, (0, 0))

    # Player movement
    player.velocity[0] = ((player.movement[0] * -1) + player.movement[1]) * 4
    player.velocity[1] = ((player.movement[2] * -1) + player.movement[3]) * 4
    player.rect.x += player.velocity[0]
    player.rect.y += player.velocity[1]


    # Prevent player from going off screen
    if player.rect.x <= 0:
        player.rect.x += 4

    if player.rect.x >= screen.get_width() - player.img.get_width():
        player.rect.x -= 4

    if player.rect.y <= 0:
        player.rect.y += 4

    if player.rect.y >= screen.get_height() - player.img.get_height():
        player.rect.y -= 4

    if not is_game_over:
        # Move toothpastes
        for i in enemies:
            if timer >= 120:
                i.rect.y -= i.velocity

        # Toothpaste appears
        for i in enemies:
            if i.rect.y >= screen.get_height():
                channel0.play(ToothpasteAppearSFX, 0)
                i.rect.y = i.img.get_height() * -1
                i.rect.x = random.randrange(0, screen.get_width() + 1)
                score += 1

        # Check for player death
        for i in enemies:
            if player.rect.colliderect(i):
                # Player died!!!
                pygame.mixer.music.stop()
                channel1.play(PlayerDeathSFX, 0)
                is_game_over = True
                timer = 0
                break

        # Render enemies
        for i in enemies:
            screen.blit(i.img, (i.rect.x, i.rect.y))

    # Render player
    screen.blit(player.img, (player.rect.x, player.rect.y))

    if is_game_over:
        # Draw game over
        screen.blit(game_over_img, (120, 80))
        # Wait 2 seconds
        if timer >= 120:
            # Reset stuff
            is_game_over = False
            score = 0
            player.rect.x = player.startX
            player.rect.y = player.startY
            pygame.mixer.music.play()
            timer = 0
            resetTOOTHPast()
    
    show_text(str(score))

    timer += 1
    clock.tick(60)
    pygame.display.update()