import pygame
import random
import math

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')

mixer.music.load("background.wav")
mixer.music.play(-1)

playerImg = icon = pygame.image.load('player.png')
playerX = 370
playerY = 480
xchange = 0

enemyImg = []
enemyX = []
enemyY = []
enxchange = []
enychange = []
no_of_enemy = 6

for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enxchange.append(4)
    enychange.append(30)


bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletxchange = 0
bulletychange = 10
bulletstate = "ready"


score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def gameover():
    over = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (200, 250))
    scores = font.render("Your Score : " + str(score), True, (255, 255, 255))
    screen.blit(scores, (270, 350))


def show_score(x, y):
    scores = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(scores, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX-bulletX), 2) + math.pow((enemyY-bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


running = True
playSound = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xchange = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xchange = -5
            if event.key == pygame.K_RIGHT:
                xchange = 5
            if event.key == pygame.K_UP:
                if bulletstate == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    playerX += xchange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(no_of_enemy):
        if enemyY[i] >= 440:
            for j in range(no_of_enemy):
                enemyY[j] = 2000
            gameover()
            if playSound:
                overSound = mixer.Sound("gameover.wav")
                overSound.play()
                playSound = False
            break

        enemyX[i] += enxchange[i]
        if enemyX[i] <= 0:
            enxchange[i] = 4
            enemyY[i] += enychange[i]
        elif enemyX[i] >= 736:
            enxchange[i] = -4
            enemyY[i] += enychange[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            expSound = mixer.Sound("explosion.wav")
            expSound.play()
            bulletY = 480
            bulletstate = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <=0:
        bulletY = 480
        bulletstate = "ready"

    if bulletstate == "fire":
        fire_bullet(bulletX ,bulletY)
        bulletY -= bulletychange

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()