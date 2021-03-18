import pygame
from board import Board


class Game:
    def __init__(self):
        self.BOARD_X = 0
        self.BOARD_Y = 0
        self.BOARD_LEN = 750
        self.WIN_WIDTH = self.BOARD_LEN + self.BOARD_X
        self.WIN_HEIGHT = self.BOARD_LEN + self.BOARD_Y
        self.MENU_X = 0
        self.MENU_Y = round(self.BOARD_LEN / 3)
        self.MENU_HEIGHT = self.BOARD_LEN - self.MENU_Y
        self.MENU_WIDTH = self.BOARD_X
        self.board = Board(self.BOARD_X, self.BOARD_Y, self.BOARD_LEN)
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.FPS = 10
        self.turn = 'Player 1'

    def click(self, pos):
        """Handles clicks outside of game board (menus and other actions)"""
        if pos[1] > self.MENU_Y:
            # Player clicked inside menu
            action = self.menu_click(pos)
        if action:
            self.end_turn()

    def menu_click(self, pos):
        """Handles button clicks inside menu"""
        # TODO: Implement action menu functionality
        action = []
        return action

    def create_rect(self, width, height, border, color, border_color):
        surf = pygame.Surface((width + border * 2, height + border * 2))
        pygame.draw.rect(surf, color, (border, border, width, height), 0)
        for i in range(1, border):
            pygame.draw.rect(surf, border_color, (border - i, border - i, width + 5, height + 5), 1)
        return surf

    def menu_text(self, font_color, small_font):
        nrows = 4
        row_ys = [10, 130, 250, 370]
        row_ys = [_ + self.MENU_Y for _ in row_ys]

        for r in range(nrows):
            if r == 0:
                txt = small_font.render(f"Turn: {self.turn}", 1, font_color)
                x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
            elif r == 1:
                txt = small_font.render("--------", 1, font_color)
                x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
            elif r == 2:
                txt = small_font.render("MOVE", 1, font_color)
                x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
            elif r == 3:
                txt = small_font.render("ABILITY", 1, font_color)
                x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
            self.win.blit(txt, (x, y))

    def draw_menu(self):
        border_color = (100, 55, 10)   # brown
        menu_color = (20, 25, 25)     # gray
        font_color = (255, 255, 255)  # white
        small_font = pygame.font.SysFont("comicsans", 24)
        alpha = 50
        border = 5
        menu = self.create_rect(self.MENU_WIDTH-border*2, self.MENU_HEIGHT-border*2, border, menu_color, border_color)
        self.win.blit(menu, (self.MENU_X, self.MENU_Y))
        self.menu_text(font_color, small_font)

    def draw(self):
        """Draws game board and menu onto screen with each frame (rate set by self.FPS)"""
        self.board.draw(self.win)
        # TODO: Implement action menu functionality
        # self.draw_menu()
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
                    pos = pygame.mouse.get_pos()
                    if pos[0] < self.BOARD_X:
                        # Player clicked outside game board
                        self.click(pos)
                    else:
                        # Player clicked inside game board
                        turn = self.board.click(pos, self.turn)
                        if turn != self.turn:
                            self.end_turn()

        pygame.quit()


if __name__ == '__main__':
    pygame.font.init()
    g = Game()
    g.run()
