from src.config import STATE
import pygame
from src.Game import Game


class HitBallGame:
    def __init__(self,  maxPoint, screenWidth, screenHeight, between, delay=10):
        self.delay = delay
        pygame.init()
        self.resolution = (screenWidth, screenHeight)
        self.maxPoint = maxPoint
        self.between = between
        # call for use text
        pygame.font.init()
        self.running = True

    def start(self):
        self.screen = pygame.display.set_mode(
            [self.resolution[0], self.resolution[1]])
        self.game = Game(self.screen, self.maxPoint,
                         resolution=self.resolution, between=self.between)

        while self.running:

            pygame.time.delay(self.delay)

            self.screen.fill((255, 255, 255))

        # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(self.game.currentStat == STATE['WIN'] or self.game.currentStat == STATE['INIT']):
                        self.game.newGame()
                    if(self.game.currentStat == STATE['START']):
                        mX, mY = event.pos
                        for index, obj in enumerate(self.game.Objs):
                            oX = obj.pX
                            oY = obj.pY
                            if (mX >= oX and mX <= oX + obj.size[0] and mY >= oY and mY <= oY + obj.size[1]):
                                self.game.hitAnimal(index)

            self.game.start()

            pygame.display.update()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def event(self, q):
        while True:
            mX, mY, side = q.get()
            print(mX, mY, side)
            if(self.game.currentStat == STATE['WIN'] or self.game.currentStat == STATE['INIT']):
                self.game.newGame()
            if(self.game.currentStat == STATE['START']):
                if(side == "LEFT"):
                    print("LEFT")
                    obj = self.game.Objs[0]
                    oX = obj.pX
                    oY = obj.pY
                    if (mX >= oX and mX <= oX + obj.size[0] and mY >= oY and mY <= oY + obj.size[1]):
                        self.game.hitAnimal(0)
                else:
                    print("RIGHT")
                    obj = self.game.Objs[1]
                    oX = obj.pX
                    oY = obj.pY
                    if (mX >= oX and mX <= oX + obj.size[0] and mY >= oY and mY <= oY + obj.size[1]):
                        self.game.hitAnimal(1)
