import pygame
import sys
pygame.init()

screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

# Player
class Player:
    def __init__(self, velocity, movement):
        self.velocity = velocity
        self.movement = movement
        self.img = pygame.image.load("player.png")
        self.rect = pygame.Rect(320, 360, self.img.get_width(), self.img.get_height())

# movement[0] = left, movement[1] = right, movement[2] = up, movement[3] = down.

player = Player([0, 0], [False, False, False, False])

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

    screen.blit(player.img, (player.rect.x, player.rect.y))
    clock.tick(60)
    pygame.display.update()