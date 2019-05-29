import pygame, sys, random, os
from pygame.locals import *

# Window starting position
position = 500, 100
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

# Record file
if not os.path.exists('record.txt'):
    file = open('record.txt', 'w')
    file.write('0')
    file.close()

file = open('record.txt')
record = int(file.read())
file.close()

# Start pygame
pygame.init()

# FPS settings
FPS = 60
fpsClock = pygame.time.Clock()

# Set up window
screenWidth = 800
screenHeight = 600
displaySurface = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pikachu Jump v1.0')

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
numFrames = 10

# Points
points = 0

# Pikachu class
class Pikachu(object):
    def __init__(self):
        self.pikaImg = [pygame.image.load('pika0.png'), pygame.image.load('pika1.png')]
        self.x = playWidth // 4
        self.y = 400
        self.minX = playX0 + playWallWidth // 2 + 1
        self.minY = playY0 + playWallWidth // 2 + 1
        self.width = self.pikaImg[0].get_width()
        self.height = self.pikaImg[0].get_height()
        self.maxX = playX0 + playWidth - playWallWidth // 2 - self.width
        self.maxY = playY0 + playHeight - playWallWidth // 2 - self.height
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
        self.width = random.randint(5, 15)
        self.height = random.randint(20, 45)
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


class Text(object):
    def __init__(self, font, text, color, x, y):
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.color = color
        self.textObject = self.font.render(self.text, True, self.color)
        self.rect = self.textObject.get_rect()
        self.rect.center = (x,y)

    def render(self, text):
        self.textObject = self.font.render(text, True, self.color)

    def show(self, display):
        display.blit(self.textObject, self.rect)


continuePlaying = True
pikachu = Pikachu()
currentTime = 0
limitTime = FPS * 3
obstacles = []


# Game texts
fontObj = pygame.font.Font('freesansbold.ttf', 32)

gameText = Text(fontObj, 'Pikachu Jump', BLUE, screenWidth//2, 20)
pointsText = Text(fontObj, 'Points: ' + str(points), RED, screenWidth // 2 - 120, screenHeight - 20)
youLoseText = Text(fontObj, 'You lose!', RED, screenWidth//2, screenHeight//2)
totalPointsText = Text(fontObj, 'Total points = ' + str(points), RED, screenWidth//2, screenHeight//2 + 30)
playAgainText = Text(fontObj, 'Press space to play again.', WHITE, screenWidth//2, screenHeight//2 + 60)
recordText = Text(fontObj, 'Record: ' + str(record), GREEN, screenWidth//2 + 120, screenHeight - 20)

# Main game loop
while True:
    if continuePlaying:
        numFrames = 10 - points//100
        if numFrames < 2:
            numFrames = 2
        displaySurface.fill(BLACK)
        pygame.draw.rect(displaySurface, WHITE, (playX0, playY0, playWidth, playHeight))
        pygame.draw.rect(displaySurface, RED, (playX0, playY0, playWidth, playHeight), playWallWidth)
        gameText.show(displaySurface)
        recordText.render('Record: ' + str(record))
        recordText.show(displaySurface)

        currentTime += 1

        if currentTime == limitTime:
            currentTime = 0
            limitTime = random.randint(FPS//2, FPS*3)
            obstacles.append(Obstacle())

        currentFrame += 1
        if currentFrame == numFrames:
            currentFrame = 0
            points += 1
            pikachu.changeSprite()

        pointsText.render('Points: ' + str(points))
        pointsText.show(displaySurface)

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
                    continuePlaying = False
                    FPS = 10
                    if points > record:
                        file = open('record.txt', 'w')
                        record = points
                        file.write(str(record))
                        file.close()

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:
                pikachu.jump()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)

    else:
        displaySurface.fill(BLACK)
        pygame.draw.rect(displaySurface, RED, (playX0, playY0, playWidth, playHeight), playWallWidth)
        totalPointsText.render('Total points = ' + str(points))

        gameText.show(displaySurface)
        youLoseText.show(displaySurface)
        totalPointsText.show(displaySurface)
        playAgainText.show(displaySurface)

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:
                FPS = 60
                continuePlaying = True
                obstacles = []
                points = 0
                pikachu = Pikachu()
                currentTime = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)
