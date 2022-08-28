from turtle import width
from pygame.locals import *
import pygame
import sys
import os


class Character:
    def __init__(self, player, x, y, data, spriteSheet, animationSteps):
        self.player = player
        self.size = data[0]
        self.imageScale = data[1]
        self.offset = data[2]
        self.animationList = self.generateImages(spriteSheet, animationSteps)
        self.action = 0  # 0:idle  1:run  2:jump  3:attack1  4:attack2  5:hit 6:death
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()
        self.rectangle = pygame.Rect((x, y, 40, 90))
        self.velocityY = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attackMethod = 0
        self.attackCooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def generateImages(self, spriteSheet, animationSteps):
        y = 0
        animationList = []
        for animation in animationSteps:
            temporaryImageList = []
            for x in range(animation):
                temporaryImage = spriteSheet.subsurface(
                    x * self.size, y * self.size,  self.size, self.size)
                temporaryImageList.append(pygame.transform.scale(
                    temporaryImage, (self.size * self.imageScale, self.size * self.imageScale)))
            animationList.append(temporaryImageList)
            y += 1
        return animationList

    def movement(self, barrierRight, barrierDown, target, screen_Height,):
        SPEED = 10
        GRAVITY = 2
        deltaX = 0
        deltaY = 0
        self.running = False
        self.attackMethod = 0
        userInput = pygame.key.get_pressed()

        if self.attacking == False:
            if self.player == 1:
                if userInput[pygame.K_a]:
                    deltaX = -SPEED
                    self.running = True
                if userInput[pygame.K_d]:
                    deltaX = SPEED
                    self.running = True
                if userInput[pygame.K_w] and self.jump == False:
                    self.velocityY = -30
                    self.jump = True
                if userInput[pygame.K_e] or userInput[pygame.K_q]:
                    self.attack(target)
                    if userInput[pygame.K_e]:
                        self.attackMethod = 1
                    if userInput[pygame.K_q]:
                        self.attackMethod = 2
            if self.player == 2:
                if userInput[pygame.K_LEFT]:
                    deltaX = -SPEED
                    self.running = True
                if userInput[pygame.K_RIGHT]:
                    deltaX = SPEED
                    self.running = True
                if userInput[pygame.K_UP] and self.jump == False:
                    self.velocityY = -30
                    self.jump = True
                # if userInput[pygame.K_SPACE] or userInput[pygame.K_l]:
                #     self.attack(target)
                #     if userInput[pygame.K_SPACE]:
                #         self.attackMethod = 1
                #     if userInput[pygame.K_l]:
                #         self.attackMethod = 2

        self.velocityY += GRAVITY
        deltaY += self.velocityY

        if self.rectangle.left + deltaX < 0:
            deltaX = - self.rectangle.left
        if self.rectangle.right + deltaX > barrierRight:
            deltaX = barrierRight - self.rectangle.right
        if self.rectangle.bottom + deltaY > screen_Height - barrierDown:
            self.velocityY = 0
            self.jump = False
            deltaY = screen_Height - barrierDown - self.rectangle.bottom

        if self.attackCooldown > 0:
            self.attackCooldown -= 1

        self.rectangle.x += deltaX
        self.rectangle.y += deltaY

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.updateAction(6)
        elif self.hit == True:
            self.updateAction(5)
        elif self.attacking == True:
            if self.attackMethod == 1:
                self.updateAction(3)
            elif self.attackMethod == 2:
                self.updateAction(4)
        elif self.jump == True:
            self.updateAction(2)
        elif self.running == True:
            self.updateAction(1)
        else:
            self.updateAction(0)

        animationCooldown = 50
        self.image = self.animationList[self.action][self.frameIndex]
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()
        if self.frameIndex >= len(self.animationList[self.action]):
            if self.alive == False:
                self.frameIndex = len(self.animationList[self.action]) - 1
            else:
                self.frameIndex = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attackCooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attackCooldown = 20

    def attack(self, target):
        if self.attackCooldown == 0:
            self.attacking = True
            attackingRectangle = pygame.Rect(
                self.rectangle.centerx - (4 * self.rectangle.width), self.rectangle.y, 4 * self.rectangle.width, self.rectangle.height)
            if attackingRectangle.colliderect(target.rectangle):
                target.health -= 10
                target.hit = True

    def updateAction(self, newAction):
        if newAction != self.action:
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

    def generate(self, surface):
        surface.blit(self.image, (self.rectangle.x -
                                  self.offset[0] * self.imageScale, self.rectangle.y - self.offset[1] * self.imageScale))
