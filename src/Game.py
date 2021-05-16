from src.Animal import Animal
from src.config import GAME, STATE
import pygame
from src.Utils import listImages

black_color = (0, 0, 0)
font_name = 'Comic Sans MS'


class Game:
    def __init__(self, screen, maxPoint, resolution, between):
        self.screen = screen
        self.points = [0, 0]
        self.maxPoint = maxPoint
        self.playerWidth = (resolution[0]-between)/2
        self.playerHeight = resolution[1]
        self.between = between

        self.resolution = resolution
        animals = listImages()
        self.animals = [animals.copy(), animals.copy()]
        self.Objs = [
            Animal(self.animals[0][0], screen, 100,
                   resolution[1], self.playerWidth),
            Animal(self.animals[1][0], screen, 100,
                   resolution[1], self.playerWidth, bound=self.playerWidth+between)
        ]
        self.currentStat = STATE['INIT']
        self.win = 3


    def start(self):
        if(self.currentStat == STATE['START']):
            # draw line center canvas
            start_pos_1 = (self.playerWidth, 0)
            end_pos_1 = (self.playerWidth, self.playerHeight)
            start_pos_2 = (self.playerWidth+self.between, 0)
            end_pos_2 = (self.playerWidth+self.between, self.playerHeight)
            pygame.draw.line(self.screen, black_color,
                             start_pos_1, end_pos_1)
            pygame.draw.line(self.screen, black_color,
                             start_pos_2, end_pos_2)

            myfont = pygame.font.SysFont(font_name, 30)
            for index, obj in enumerate(self.Objs):
                obj.updatePosition()
                self.screen.blit(myfont.render(
                    ('Point : ' + str(self.points[index])), False, black_color), (obj.bound+15, 15))
        if(self.currentStat == STATE['WIN']):
            myfont = pygame.font.SysFont(font_name, 80)
            winText = myfont.render(
                'Player '+str(self.win+1) + ' Win', False, black_color)
            winTextRect = winText.get_rect(
                center=(GAME['WIDTH']/2, GAME['HEIGHT']/2))
            self.screen.blit(winText, winTextRect)
            newGame = myfont.render(
                'Hit Ball to New Game', False, black_color)
            newGameRect = newGame.get_rect(
                center=(GAME['WIDTH']/2, GAME['HEIGHT']/2 + 90))
            self.screen.blit(newGame, newGameRect)
        if(self.currentStat == STATE['INIT']):
            myfont = pygame.font.SysFont(font_name, 80)
            newGame = myfont.render(
                'Hit Ball to Start Game', False, black_color)
            newGameRect = newGame.get_rect(
                center=(GAME['WIDTH']/2, GAME['HEIGHT']/2))
            self.screen.blit(newGame, newGameRect)

    def hitAnimal(self, index):
        print("hit Animal")
        del self.animals[index][0]
        self.Objs[index].rePosition(self.animals[index][0])
        self.points[index] = self.points[index] + 1
        if(self.points[index] >= self.maxPoint):
            self.currentStat = STATE['WIN']
            self.win = index

    def newGame(self):
        print('newGame')
        animals = listImages()
        self.animals = [animals.copy(), animals.copy()]
        self.Objs = [
            Animal(self.animals[0][0], self.screen, 100,
                   self.resolution[1], self.playerWidth),
            Animal(self.animals[1][0], self.screen, 100,
                   self.resolution[1], self.playerWidth, bound=self.playerWidth+self.between)
        ]
        self.points = [0, 0]
        self.currentStat = STATE['START']
