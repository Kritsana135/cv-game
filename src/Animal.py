import pygame
from os import path
from src.Utils import randomVector, randomDirection


class Animal:
    def __init__(self, obj_name, screen, size, height, width, bound=0):
        self.size = self.loadImg(obj_name)
        self.screen = screen
        self.pX, self.pY, self.direction = randomVector(
            width, height, self.size, bound)
        self.width = width
        self.height = height
        self.bound = bound
        self.sX, self.sY = randomDirection()

    def loadImg(self, obj_name):
        img = pygame.image.load(path.join("./assets/images/", obj_name))
        self.obj = pygame.transform.scale(
            img, (int(img.get_width()/5), int(img.get_height()/5)))
        return (int(img.get_width()/5), int(img.get_height()/5))

    def placeObj(self, x, y):
        self.screen.blit(self.obj, (x, y))

    def rePosition(self, obj_name):
        self.size = self.loadImg(obj_name)
        self.pX, self.pY, self.direction = randomVector(
            self.width, self.height, self.size, self.bound)
        self.sX, self.sY = randomDirection()

    def updatePosition(self):
        self.placeObj(self.pX, self.pY)
        self.pX += self.sX
        self.pY += self.sY

        # wall on left or right
        if(self.pX + self.size[0] > self.width+self.bound or self.pX < self.bound):
            self.sX = -self.sX

        # top or bottom
        if(self.pY < 0 or self.pY + self.size[1] > self.height):
            self.sY = -self.sY
