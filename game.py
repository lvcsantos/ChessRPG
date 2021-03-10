import pygame
from board import Board


class Game:
    def __init__(self):
        self.WIDTH = 750
        self.HEIGHT = 750
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.board = Board(0, 0, self.WIDTH, self.HEIGHT)
        self.FPS = 10
        self.turn = 'Player 1'

    def click(self, pos):
        """Handles clicks outside of game board (menus and other actions)"""
        pass

    def draw(self):
        self.board.draw(self.win)
        pygame.display.update()

    def end_turn(self):
        if self.turn == 'Player 1':
            self.turn = 'Player 2'
        else:
            self.turn = 'Player 1'
        self.board.pieceSelected = False

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(self.FPS)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if pygame.mouse.get_pressed()[0]:
                    turn = self.board.click(pygame.mouse.get_pos(), self.turn)
                    if turn != self.turn:
                        self.end_turn()

        pygame.quit()


if __name__ == '__main__':
    # pygame.font.init()
    g = Game()
    g.run()
