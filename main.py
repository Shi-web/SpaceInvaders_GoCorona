import pygame
import math
import random
from pygame import mixer
# Initialising pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('BG.png').convert()

# Title and icon
pygame.display.set_caption("Go Corona ")
icon = pygame.image.load('safety-suit.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('doctor.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('coronavirus.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(10)

# Vaccine
vaccineImg = pygame.image.load('syringe (2).png')
vaccineX = 0
vaccineY = 480
vaccineX_change = 0
vaccineY_change = 1
vaccine_state = "ready"

# Score Font

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_vaccine(x, y):
    global vaccine_state
    vaccine_state = "fire"
    screen.blit(vaccineImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, vaccineX, vaccineY):
    distance = math.sqrt((math.pow(enemyX - vaccineX, 2)) + (math.pow(enemyY - vaccineY, 2)))
    if distance <= 27:
        return True
    else:
        return False


# GameLoop
running = True
while running:

    # RGB- RED GREEN BLUE
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4

            if event.key == pygame.K_SPACE:
                if vaccine_state == "ready":
                    vaccine_sound = mixer.Sound('laser.wav')
                    vaccine_sound.play()
                    vaccineX = playerX
                    fire_vaccine(vaccineX, vaccineY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.type == pygame.K_SPACE:
                playerX_change = 0
                vaccineY = 0

    # Checking for boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], vaccineX, vaccineY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            vaccineY = 480
            vaccine_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Vaccine Movement
    if vaccineY <= 0:
        vaccineY = 480
        vaccine_state = "ready"
    if vaccine_state == "fire":
        fire_vaccine(vaccineX, vaccineY)
        vaccineY -= vaccineY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
