import math
import random

import pygame

pygame.init()


# Paint the player to the screen
def paint_player(x, y):
    gameDisplay.blit(playerImg, (x, y))


# Paint the enemy to the screen
def paint_enemy(img, x, y):
    gameDisplay.blit(img, (x, y))


# start displaying the score board
def display_score(x, y):
    score = font.render("SCORE : " + str(gameScore), True, (192, 194, 196))
    gameDisplay.blit(score, (x, y))


def game_init():
    global playerX, playerY, pXChange, pYChange, enemyX, enemyY, enemyImg, eXMovement, eYMovement
    playerX = dispWidth // 2 - 32
    playerY = dispHeight - 80
    pXChange = 0
    pYChange = 0
    enemyImg = []
    enemyX = []
    enemyY = []
    eXMovement = []
    eYMovement = []
    eYMovement = []
    for index in range(no_of_enemies):
        enemyImg.append(pygame.image.load('resources/images/alien.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(20, 100))
        eXMovement.append(random.randint(3, 7))
        eYMovement.append(.1 * (random.randint(1, 4)))


# Functions to detect collision


def isbulletcollision(bulletx, bullety, enemyx, enemyy):
    global bStatus
    d = math.sqrt(math.pow((enemyx + 16 - bulletx), 2) + math.pow((enemyy + 32 - bullety), 2))
    if d <= 28:
        bStatus = "ready"
        pygame.mixer.Sound('resources/sounds/explosion.wav').play()
        return True
    return False


def isplayercollision(playerx, playery, enemyx, enemyy):
    d = math.sqrt(math.pow((enemyx - playerx), 2) + math.pow((enemyy - playery), 2))
    if d <= 48:
        return True
    return False


# Player bounds


def boundplayer():
    global playerX
    global playerY
    # bound X axis
    if playerX < 0:
        playerX = 0
    elif playerX > dispWidth - 64:
        playerX = dispWidth - 64
    # bound Y axis
    if playerY < 0:
        playerY = 0
    elif playerY > dispHeight - 64:
        playerY = dispHeight - 64


# reset enemy position
def resetenemy():
    return [random.randint(0, 736), random.randint(20, 100), random.randint(3, 7), (.1 * (random.randint(1, 4)))]


# enemy bounds
def boundenemy(index):
    global enemyX, eXMovement
    if enemyX[index] <= 0:
        eXMovement[index] = eXMovement[index] * -1
    if enemyX[index] >= dispWidth - 64:
        eXMovement[index] = -eXMovement[index]


# Bullet bounds
def boundbullets():
    global bStatus
    if bulletY <= 0:
        bStatus = "ready"


dispWidth = 1080
dispHeight = 720
gameScore = 0

# Creating the canvas
gameDisplay = pygame.display.set_mode((dispWidth, dispHeight))

# Setting game background
background = pygame.image.load('resources/images/space.jpg')
background = pygame.transform.smoothscale(background, (dispWidth, dispHeight))
background.set_alpha(192)

# setting background music
pygame.mixer.music.load('resources/sounds/background.wav')
pygame.mixer.music.play(-1)

# Title and icon
game_icon = pygame.image.load("resources/images/ufo.png")
pygame.display.set_caption('Space Shooter')
pygame.display.set_icon(game_icon)

# Game clock
clock = pygame.time.Clock()

# font to render
font = pygame.font.Font('freesansbold.ttf', 20)
gameOverfont = pygame.font.Font('freesansbold.ttf', 48)
# Game Over card

gameOverBack = pygame.image.load('resources/images/gameovr.jpg')
gameOverBack = pygame.transform.smoothscale(gameOverBack, (1000, 600))
gameOverText = gameOverfont.render("GAME OVER", True, (255, 255, 255))
# player
playerImg = pygame.image.load('resources/images/player.png')
playerX = (dispWidth // 2) - 32
playerY = dispHeight - 20
pXChange = 0
pYChange = 0
pPosMovement = 5
pNegMovement = -5

# enemy
enemyImg = []
enemyX = []
enemyY = []
eXMovement = []
eYMovement = []
no_of_enemies = 10

# Bullet
bulletImg = pygame.image.load('resources/images/bullet.png')
bulletX = 0
bulletY = 0
bXMovement = 0
bYMovement = -8
bStatus = "ready"

if __name__ == '__main__':
    game_init()
    crashed = False
    isAlive = True
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                crashed = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                isKeyDown = True
                if event.key == pygame.K_UP:
                    pYChange = pNegMovement
                if event.key == pygame.K_DOWN:
                    pYChange = pPosMovement
                if event.key == pygame.K_RIGHT:
                    pXChange = pPosMovement
                if event.key == pygame.K_LEFT:
                    pXChange = pNegMovement
                if bStatus == "ready" and event.key == pygame.K_SPACE:
                    pygame.mixer.Sound('resources/sounds/laser.wav').play()
                    bulletX = playerX
                    bulletY = playerY
                    bStatus = "fire"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pYChange = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    pXChange = 0
            if (not isAlive) and (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN):
                # if event.key == pygame.BUTTON_LEFT:
                isAlive = True
                game_init()

        if isAlive:
            gameDisplay.fill((62, 64, 62))
            gameDisplay.blit(background, (0, 0))
            display_score(10, 10)
            paint_player(playerX, playerY)
            # Player Movement
            playerX += pXChange
            playerY += pYChange
            # Enemy Movement
            for i in range(no_of_enemies):
                paint_enemy(enemyImg[i], enemyX[i], enemyY[i])
                enemyX[i] += eXMovement[i]
                enemyY[i] += eYMovement[i]
                boundenemy(i)
                if bStatus == "fire":
                    if isbulletcollision(bulletx=bulletX, bullety=bulletY, enemyx=enemyX[i], enemyy=enemyY[i]):
                        [enemyX[i], enemyY[i], eXMovement[i], eYMovement[i]] = resetenemy()
                        gameScore += 1

                if isplayercollision(playerx=playerX, playery=playerY, enemyx=enemyX[i], enemyy=enemyY[i]):
                    isAlive = False
                if enemyY[i] >= dispHeight - 64:
                    isAlive = False
            boundplayer()
            # Bullet Movement
            if bStatus == "fire":
                bulletY += bYMovement
                gameDisplay.blit(bulletImg, (bulletX + 16, bulletY - 20))
                boundbullets()

        else:
            gameDisplay.fill((255, 0, 0))
            gameDisplay.blit(gameOverBack, (-100, 0))
            gameDisplay.blit(gameOverText, (250, 200))
            display_score(350, 280)
        pygame.display.update()
        clock.tick(60)
    pygame.display.update()
    pygame.quit()
    quit()
