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

screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

timer = 0

# Player
class Player:
    def __init__(self, velocity, movement):
        self.velocity = velocity
        self.movement = movement
        self.img = pygame.image.load("player.png")
        self.rect = pygame.Rect(320, 360, self.img.get_width(), self.img.get_height())

class Enemy:
    def __init__(self, velocity):
        self.velocity = velocity
        self.img = pygame.image.load("toothpaste.png")
        self.rect = pygame.Rect(random.randrange(0, screen.get_width() + 1), self.img.get_height() * -1, self.img.get_width(), self.img.get_height())

# movement[0] = left, movement[1] = right, movement[2] = up, movement[3] = down.

player = Player([0, 0], [False, False, False, False])

# Enemies
enemy1 = Enemy(-12)
enemy2 = Enemy(-11)
enemy3 = Enemy(-10)
enemy4 = Enemy(-9)
enemy5 = Enemy(-8)
enemy6 = Enemy(-7)
enemy7 = Enemy(-6)
enemy8 = Enemy(-5)
enemy9 = Enemy(-4)
enemy10 = Enemy(-3)

enemies = [
    enemy1,
    enemy2,
    enemy3,
    enemy4,
    enemy5,
    enemy6,
    enemy7,
    enemy8,
    enemy9,
    enemy10
]

# Game over
game_over_img = pygame.image.load("gameovertext.png")
is_game_over = False

def game_over():
    screen.blit(game_over_img, (120, 80))

while True:
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

    player.velocity[0] = ((player.movement[0] * -1) + player.movement[1]) * 4
    player.velocity[1] = ((player.movement[2] * -1) + player.movement[3]) * 4
    player.rect.x += player.velocity[0]
    player.rect.y += player.velocity[1]

    screen.fill((0, 200, 255))

    if player.rect.x <= 0:
        player.rect.x += 4

    if player.rect.x >= screen.get_width() - player.img.get_width():
        player.rect.x -= 4

    if player.rect.y <= 0:
        player.rect.y += 4

    if player.rect.y >= screen.get_height() - player.img.get_height():
        player.rect.y -= 4

    for i in enemies:
        if timer >= 60:
            i.rect.y -= i.velocity

    if not(is_game_over):
        for i in enemies:
            if i.rect.y >= screen.get_height():
                channel0.play(ToothpasteAppearSFX, 0)
                i.rect.y = i.img.get_height() * -1
                i.rect.x = random.randrange(0, screen.get_width() + 1)

    if not(is_game_over):
        for i in enemies:
            if player.rect.colliderect(i):
                pygame.mixer.music.stop()
                channel1.play(PlayerDeathSFX, 0)
                is_game_over = True

    if not(is_game_over):
        for i in enemies:
            if timer >= 60:
                screen.blit(i.img, (i.rect.x, i.rect.y))

    screen.blit(player.img, (player.rect.x, player.rect.y))

    if is_game_over:
        game_over()

    timer += 1
    clock.tick(60)
    pygame.display.update()