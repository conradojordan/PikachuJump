import pygame, sys, random
from pygame.locals import *

pygame.init()

# FPS settings
FPS = 60
fpsClock = pygame.time.Clock()

# Set up window
screenWidth = 800
screenHeight = 600
displaySurface = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pikachu Jump v0.9')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Delimiting play area
playWidth = 700
playHeight = 500
playX0 = 50
playY0 = 50
playWallWidth = 10

# Pikachu sprite frames duration
currentFrame = 0
numFrames = 8

# Points
points = 0

# Pikachu class
class Pikachu(object):
    def __init__(self):
        self.pikaImg = [pygame.image.load('pika0.png'), pygame.image.load('pika1.png')]
        self.x = playWidth//4
        self.y = 400
        self.minX = playX0 + playWallWidth//2 + 1
        self.minY = playY0 + playWallWidth//2 + 1
        self.width = self.pikaImg[0].get_width()
        self.height = self.pikaImg[0].get_height()
        self.maxX = playX0 + playWidth - playWallWidth//2 - self.width
        self.maxY = playY0 + playHeight - playWallWidth//2 - self.height
        self.velX = 0
        self.velY = 0
        self.maxVelX = 3
        self.maxVelY = 8
        self.acelX = 0
        self.acelY = 1
        self.image = 0
    
    def changeSprite(self):
        if self.image:
            self.image = 0
        else:
            self.image = 1

    def updatePosition(self):
        self.x += self.velX
        if self.x > self.maxX:
            self.x = self.minX
    
        self.y += self.velY
        if self.y > self.maxY:
            self.y = self.maxY
        elif self.y < self.minY:
            self.y = self.minY
            self.velY = 0
    
        self.velX += self.acelX
        if self.velX > self.maxVelX:
            self.velX = self.maxVelX
    
        self.velY += self.acelY
        if self.velY > self.maxVelY:
            self.velY = self.maxVelY

    def jump(self):
        global pikachu
        if self.y == self.maxY:
            self.velY = -15

class Obstacle(object):
    def __init__(self):
        self.width = 10
        self.height = 30
        self.minX = playX0 + playWallWidth // 2 + 1
        self.minY = playY0 + playWallWidth // 2 + 1
        self.maxX = playX0 + playWidth - playWallWidth // 2 - self.width
        self.maxY = playY0 + playHeight - playWallWidth // 2 - self.height
        self.x = self.maxX
        self.y = self.maxY
        self.velX = -(points//100+3)
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.destroy = False
        pygame.draw.rect(displaySurface, BLUE, (self.x, self.y, self.width, self.height))

    def updatePosition(self):
        self.x += self.velX
        if self.x < self.minX:
            self.destroy = True

pikachu = Pikachu()
currentTime = 0
limitTime = FPS*3
obstacles = []
lose = False

fontObj = pygame.font.Font('freesansbold.ttf', 32)
gameText = fontObj.render('Pokémon Jump', True, BLUE)
gameTextRect = gameText.get_rect()
gameTextRect.center = (width//2, 20)
currentPoints = fontObj.render('Points: ' + str(points), True, RED)
currentPointsRect = currentPoints.get_rect()
currentPointsRect.center = (width//2, height - 20)


# Main game loop
while not lose:
    displaySurface.fill(BLACK)
    pygame.draw.rect(displaySurface, RED, (playX0, playY0, playWidth, playHeight), playWallWidth)
    displaySurface.blit(gameText, gameTextRect)

    currentTime += 1

    if currentTime == limitTime:
        currentTime = 0
        limitTime = random.randint(FPS//2,FPS*3)
        #limitTime = random.randint(FPS//2-((FPS//2)/(points//100+1)),FPS*3)
        obstacles.append(Obstacle())

    currentFrame += 1
    if currentFrame == numFrames:
        currentFrame = 0
        points += 1
        pikachu.changeSprite()

    currentPoints = fontObj.render('Points: ' + str(points), True, RED)
    displaySurface.blit(currentPoints, currentPointsRect)

    pikachu.updatePosition()
    displaySurface.blit(pikachu.pikaImg[pikachu.image], (pikachu.x, pikachu.y))

    # Update obstacles positions
    for obstacle in obstacles:
        obstacle.updatePosition()
        if obstacle.destroy:
            obstacles.pop(obstacles.index(obstacle))
        else:
            pygame.draw.rect(displaySurface, BLUE, (obstacle.x, obstacle.y, obstacle.width, obstacle.height))

    for obstacle in obstacles:
        if obstacle.x < pikachu.x + pikachu.width and obstacle.x > pikachu.x:
            if obstacle.y < pikachu.y + pikachu.height and obstacle.y + obstacle.height > pikachu.y:
                lose = True

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE:
            pikachu.jump()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)

youLose = fontObj.render('You lose!', True, RED)
youLoseRect = youLose.get_rect()
youLoseRect.center = (width//2, height//2)

totalPoints = fontObj.render('Total points = ' + str(points), True, RED)
totalPointsRect = totalPoints.get_rect()
totalPointsRect.center = (width//2, height//2 + 30)



while True:
    displaySurface.fill(BLACK)
    pygame.draw.rect(displaySurface, RED, (playX0, playY0, playWidth, playHeight), playWallWidth)
    displaySurface.blit(gameText, gameTextRect)
    displaySurface.blit(youLose, youLoseRect)
    displaySurface.blit(totalPoints, totalPointsRect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()