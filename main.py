from player import Character
import button
from turtle import width
from pygame.locals import *
import pygame
import sys
import math
import os

pygame.init()
fontHeader = pygame.font.Font("font.ttf", 60, bold=True)
font = pygame.font.Font("font.ttf", 15, bold=True)


screenWidth = 1000
screenHeight = 500
scroll = 0
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Testing Game")
monitorSize = [pygame.display.Info().current_w,
               pygame.display.Info().current_h]


startGame = False
fullscreen = False
startImage = pygame.image.load("start_btn.png").convert_alpha()
exitImage = pygame.image.load("exit_btn.png").convert_alpha()

groundImage = pygame.image.load("ground.png").convert_alpha()
groundWidth = groundImage.get_width()
groundHeight = groundImage.get_height()
background = pygame.image.load("background.png").convert_alpha()
backgroundWidth = background.get_width()
backgroundRectangle = background.get_rect()
tiles = math.ceil(screenWidth / backgroundWidth) + 1
background = pygame.transform.scale(
    background, (screenWidth, screenHeight)).convert_alpha()

FPS = 60
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
characterSize = 150
characterScale = 3
characterOffset = [100, groundHeight]
characterData = [characterSize, characterScale, characterOffset]

backgroundImages = []
characterSheet = pygame.image.load("huntress.png").convert_alpha()
characterAnimationSteps = [8, 8, 2, 5, 5, 3, 8]


for image in range(1, 6):
    backgroundImage = pygame.transform.scale(pygame.image.load(
        (f"plx-{image}.png")), (screenWidth, screenHeight)).convert_alpha()
    backgroundImages.append(backgroundImage)
backgroundWidth = backgroundImages[0].get_width()


def generateBackground():
    for i in range(5):
        for j in backgroundImages:
            screen.blit(j, ((i * backgroundWidth), 0))


def generateGround():
    for k in range(15):
        screen.blit(groundImage, ((k * groundWidth),
                                  screenHeight - groundHeight))


def healthBars(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 204, 24))
    pygame.draw.rect(screen, RED, (x, y, 200, 20))
    pygame.draw.rect(screen, YELLOW, (x, y, 200 * ratio, 20))


def generateText(text, font, textColor, x, y):
    image = font.render(text, True, textColor)
    screen.blit(image, (x, y))


startButton = button.Button(
    screenWidth // 2 - 130, screenHeight // 2 - 100, startImage, 1)
exitButton = button.Button(
    screenWidth // 2 - 110, screenHeight // 2 + 50, exitImage, 1)


character1 = Character(1, 300, groundHeight, characterData,
                       characterSheet, characterAnimationSteps)
character2 = Character(2, 600, groundHeight, characterData,
                       characterSheet, characterAnimationSteps)

run = True
while run:
    clock.tick(60)
    if startGame == False:
        for i in range(0, tiles):
            screen.blit(background, (i * backgroundWidth + scroll, 0))
        generateText("Created by Cajaun Campbell", font, WHITE, 600, 450)
        generateText("Press F to enter fullscreen", font, WHITE,
                     screenWidth // 2 - 200, screenHeight // 2 + 20)
        generateText("Main Menu", fontHeader, WHITE,
                     screenWidth // 2 - 250, screenHeight // 2 - 200)
        scroll -= 1
        if abs(scroll) > backgroundWidth:
            scroll = 0
        if startButton.draw(screen):
            startGame = True
        if exitButton.draw(screen):
            run = False
    else:
        generateBackground()
        generateGround()
        healthBars(character1.health, 780, 20)
        character1.movement(screenWidth,
                            groundHeight, character2, screenHeight)
        character1.update()
        character1.generate(screen)
        character2.movement(screenWidth,
                            groundHeight, character1, screenHeight)
        character2.update()
        character2.generate(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(
                        monitorSize, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(
                        (screen.get_width(), screen.get_height()), pygame.RESIZABLE)

    pygame.display.update()
pygame.quit()
