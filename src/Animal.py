import pygame
from os import path
from src.Utils import randomVector, randomDirection


class Animal:
    def __init__(self, obj_name, screen, size, height, width, bound=0):
        self.obj = pygame.image.load(path.join("./assets/images/lion.png"))
        self.obj = pygame.transform.scale(self.obj, (size, size))
        self.screen = screen
        self.pX, self.pY, self.direction = randomVector(
            width, height, size, bound)
        self.size = size
        self.width = width
        self.height = height
        self.bound = bound
        self.sX, self.sY = randomDirection()

    def placeObj(self, x, y):
        self.screen.blit(self.obj, (x, y))

    def rePosition(self):
        self.pX, self.pY, self.direction = randomVector(
            self.width, self.height, self.size, self.bound)
        self.sX, self.sY = randomDirection()

    def updatePosition(self):
        self.placeObj(self.pX, self.pY)
        self.pX += self.sX
        self.pY += self.sY

        # wall on left or right
        if(self.pX + self.size > self.width+self.bound or self.pX < self.bound):
            self.sX = -self.sX

        # top or bottom
        if(self.pY < 0 or self.pY + self.size > self.height):
            self.sY = -self.sY
