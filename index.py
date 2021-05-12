from src.config import STATE
import pygame
from src.Game import Game


class HitBallGame:
    def __init__(self, delay=10, maxPoint=10, screenWidth=800, screenHeight=600, between=20):
        self.delay = delay
        pygame.init()
        self.resolution = (screenWidth, screenHeight)
        self.screen = pygame.display.set_mode([screenWidth, screenHeight])
        self.game = Game(self.screen, maxPoint,
                         resolution=self.resolution, between=between)
        # call for use text
        pygame.font.init()
        self.running = True

    def start(self):
        while self.running:
            pygame.time.delay(self.delay)

            self.screen.fill((255, 255, 255))

        # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(self.game.currentStat == STATE['WIN'] or self.game.currentStat == STATE['INIT']):
                        self.game.newGame()
                    if(self.game.currentStat == STATE['START']):
                        mX, mY = event.pos
                        for index, obj in enumerate(self.game.Objs):
                            oX = obj.pX
                            oY = obj.pY
                            if (mX >= oX and mX <= oX + obj.size and mY >= oY and mY <= oY + obj.size):
                                self.game.hitAnimal(index)

            self.game.start()

            pygame.display.update()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()

    def event(x, y, side):
        print(x, y, side)


if __name__ == "__main__":
    HitBallGame(maxPoint=2, between=80).start()
