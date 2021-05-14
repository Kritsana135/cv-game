from random import randint, choice, shuffle
import pygame
from src.config import GAME
import os


def randomVector(WIDTH, HEIGHT, OBJECT_SIZE, BOUND):
    x = randint(BOUND, (WIDTH-OBJECT_SIZE[0])+BOUND)
    y = randint(0, (HEIGHT-OBJECT_SIZE[1]))
    direction = choice([1, -1])
    return (x, y, direction)


def randomDirection():
    x = choice([1, 0, -1])
    y = choice([1, 0, -1])
    if(x != 0 and y != 0):
        return (x, y)
    else:
        return randomDirection()


def centerText(text, screen, color=(0, 0, 0)):
    myfont = pygame.font.SysFont('Comic Sans MS', 80)
    winText = myfont.render(text, False, color)
    winTextRect = winText.get_rect(
        center=(GAME['WIDTH']/2, GAME['HEIGHT']/2))
    screen.blit(winText, winTextRect)


def listImages():
    filenames = []
    for root, dirs, files in os.walk("./assets/images"):
        for filename in files:
            filenames.append(filename)
    shuffle(filenames)
    return filenames
