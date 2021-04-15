import pygame
from board import Board


class Game:
    def __init__(self):
        self.BOARD_X = 250
        self.BOARD_Y = 0
        self.BOARD_LEN = 750
        self.GRID_LEN = 9
        self.TILE_SIZE = self.BOARD_LEN / self.GRID_LEN
        self.WIN_WIDTH = self.BOARD_LEN + self.BOARD_X
        self.WIN_HEIGHT = self.BOARD_LEN + self.BOARD_Y
        self.MENU_X = 0
        self.MENU_Y = round(self.BOARD_LEN / 3)
        self.MENU_HEIGHT = self.BOARD_LEN - self.MENU_Y
        self.MENU_WIDTH = self.BOARD_X
        self.MENU_TEXT_Y = [30, 145, 270, 395]
        self.MENU_NROWS = len(self.MENU_TEXT_Y)
        self.MENU_ROWS_YS = [[0, self.MENU_HEIGHT - 3 * int(self.MENU_HEIGHT / 4)],
                    [self.MENU_HEIGHT - 3 * int(self.MENU_HEIGHT / 4), self.MENU_HEIGHT - 2*int(self.MENU_HEIGHT/4)],
                    [self.MENU_HEIGHT - 2 * int(self.MENU_HEIGHT / 4), self.MENU_HEIGHT - int(self.MENU_HEIGHT/4)],
                    [self.MENU_HEIGHT - int(self.MENU_HEIGHT / 4), self.MENU_HEIGHT]]
        self.MENU_ROW_HEIGHT = self.MENU_ROWS_YS[0][1]
        self.TOP_MENU_HEIGHT = self.MENU_Y
        self.FPS = 30
        self.board = Board(self.BOARD_X, self.BOARD_Y, self.BOARD_LEN, self.GRID_LEN)
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.menu_font = pygame.font.SysFont("comicsans", 24)
        self.menu_state = 'main'  # 'idle', 'action', 'abilities', 'end'
        self.turn = 'Player 1'
        self.action = 'idle'

    def click(self, pos):
        """Handles clicks outside of game board (menus and other actions)"""
        # TODO: move piece and highlight valid_moves only after MOVE button click
        # TODO: implement valid_targets highlight for abstract ability squares
        # TODO: graphic for click event, different color than mouse hover(?)

        if pos[1] > self.MENU_Y:
            # Player clicked inside menu
            y = pos[1] - self.MENU_Y
            if self.MENU_ROWS_YS[0][0] < y < self.MENU_ROWS_YS[0][1]:
                # Player clicked on 1st menu button
                if self.menu_state == 'abilities':
                    # BACK button
                    self.menu_state = 'main'
                    self.action = 'idle'
                if self.menu_state == 'action':
                    # CANCEL button
                    if self.action == 'move':
                        self.menu_state = 'main'
                        self.action = 'idle'
                    else:
                        self.menu_state = 'abilities'
                        self.action = 'idle'
            elif self.MENU_ROWS_YS[1][0] < y < self.MENU_ROWS_YS[1][1]:
                # Player clicked on 2nd menu button
                if self.menu_state == 'abilities':
                    # BASIC ability
                    self.menu_state = 'action'
                    self.action = 'basic'
            elif self.MENU_ROWS_YS[2][0] < y < self.MENU_ROWS_YS[2][1]:
                # Player clicked on 3rd menu button
                if self.menu_state == 'abilities':
                    # SPECIAL ability
                    self.menu_state = 'action'
                    self.action = 'special'
                if self.menu_state == 'main':
                    # MOVE button
                    if self.board.pieceSelected:
                        self.menu_state = 'action'
                        self.action = 'move'
            elif self.MENU_ROWS_YS[3][0] < y < self.MENU_ROWS_YS[3][1]:
                # Player clicked on 4th menu button
                if self.menu_state == 'abilities':
                    # UTILITY ability
                    self.menu_state = 'action'
                    self.action = 'utility'
                if self.menu_state == 'main':
                    if self.board.pieceSelected:
                        self.menu_state = 'abilities'
        else:
            # Player clicked on 'End Turn' button
            self.end_turn()

    def check_menu_hover(self, pos):
        row_i = None
        y = pos[1] - self.MENU_Y
        for r in range(self.MENU_NROWS):
            if self.MENU_ROWS_YS[r][0] < y < self.MENU_ROWS_YS[r][1]:
                row_i = r
        return row_i

    def grid2pos(self, row, col, offset=True):
        if offset:
            y = row * self.TILE_SIZE + self.Y_OFFSET + self.BOARD_Y
        else:
            y = row * self.TILE_SIZE + self.BOARD_Y
        x = col * self.TILE_SIZE + self.BOARD_X
        return x, y

    def menu2pos(self, menu_row):
        x = self.MENU_X
        y = self.MENU_ROWS_YS[menu_row][0]
        x_y = (x, y)
        return x_y

    def draw_rect(self, width, height, border, color, border_color):
        surf = pygame.Surface((width + border * 2, height + border * 2))
        pygame.draw.rect(surf, color, (border, border, width, height), 0)
        for i in range(1, border):
            pygame.draw.rect(surf, border_color, (border - i, border - i, width + 5, height + 5), 1)
        return surf

    def draw_aura(self, mode='rect', loc='menu', menu_row=None, grid_pos=None):
        """General draw aura highlight for menu button hover/click and pieces/squares on board
        Inputs
            mode = can be either 'rect' or 'circle'
            loc  = can be either 'grid' or 'menu'
        menu_row = if loc is 'menu', menu_row is the row index to highlight
        grid_pos = if loc is 'grid', grid_pos is the grid index to highlight
        """
        aura_color = (100, 255, 100)
        tile_color = (255, 100, 0)
        alpha = 50
        if mode == 'rect':
            if loc == 'grid':
                tile_offset = 2
                tile_size = self.TILE_SIZE + tile_offset
                rect = pygame.Rect(0, 0, tile_size, tile_size)
                if not grid_pos:
                    raise Exception('If drawing on grid, need grid_pos')
                else:
                    surf = pygame.Surface((tile_size, tile_size))
                    surf.set_alpha(alpha)
                    pygame.draw.rect(surf, tile_color, rect)
                    self.win.blit(surf, self.grid2pos(grid_pos[0], grid_pos[1], offset=False))
            elif loc == 'menu':
                if not menu_row:
                    raise Exception('If drawing on menu, need menu_row')
                else:
                    rect = pygame.Rect(0, 0, self.MENU_ROW_HEIGHT, self.MENU_WIDTH)
                    surf = pygame.Surface((self.MENU_ROW_HEIGHT, self.MENU_WIDTH))
                    surf.set_alpha(alpha)
                    pygame.draw.rect(surf, aura_color, rect)
                    print(menu_row)
                    print(self.menu2pos(menu_row))
                    self.win.blit(surf, self.menu2pos(menu_row))
            else:
                raise Exception('Unrecognizable loc parameter input')
        elif mode == 'circle':
            center = ((self.TILE_SIZE / 2), (self.TILE_SIZE / 2))
            radius, width = 40, 0
        else:
            raise Exception('Unrecognizable mode parameter input')

    def get_hp(self, player):
        hp = {}
        for r in range(self.GRID_LEN):
            for c in range(self.GRID_LEN):
                if self.board.board[r][c] != 0:
                    current_piece = self.board.board[r][c]
                    if current_piece.player == player:
                        hp[current_piece.name] = current_piece.hp
        txt = f"  {hp['Cleric']}      {hp['Paladin']}      {hp['Ranger']}      {hp['Rogue']}      {hp['Wizard']}"
        return txt

    def top_menu_text(self, font_color):
        # Top menu shows player units and HP
        row_ys = [30,50,70, 150,170,190]
        x = 10
        for r in range(len(row_ys)):
            y = row_ys[r]
            if r == 0:
                txt = self.menu_font.render("Player 1: Red", False, font_color)
            elif r == 1:
                txt = self.menu_font.render(" Cle   Pal   Ran   Rog   Wiz ", False, font_color)
            elif r == 2:
                hp_txt = self.get_hp('Player 1')
                txt = self.menu_font.render(hp_txt, False, font_color)
            elif r == 3:
                txt = self.menu_font.render("Player 2: Blue", False, font_color)
            elif r == 4:
                txt = self.menu_font.render(" Cle   Pal   Ran   Rog   Wiz ", False, font_color)
            elif r == 5:
                hp_txt = self.get_hp('Player 2')
                txt = self.menu_font.render(hp_txt, False, font_color)
            self.win.blit(txt, (x, y))

    def menu_text(self, font_color):
        row_ys = [_ + self.MENU_Y for _ in self.MENU_TEXT_Y]

        for r in range(self.MENU_NROWS):
            if self.menu_state == 'main':
                # Main menu shows player turn and MOVE/ABILITY buttons; at start of game, new turn, or back button
                if r == 0:
                    txt = self.menu_font.render(f"Turn: {self.turn}", False, font_color)
                    x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
                elif r == 1:
                    txt = self.menu_font.render("--------", False, font_color)
                    x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
                elif r == 2:
                    txt = self.menu_font.render("MOVE", False, font_color)
                    x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
                elif r == 3:
                    txt = self.menu_font.render("ABILITY", False, font_color)
                    x, y = self.MENU_WIDTH / 2 - txt.get_width() / 2, row_ys[r]
                self.win.blit(txt, (x, y))

            elif self.menu_state == 'action':
                # During an action, the menu has a cancel button and shows text based on action
                x = 10
                if r == 0:
                    "Cancel button"
                    txt = self.menu_font.render("CANCEL", False, font_color)
                    y = row_ys[r]
                    self.win.blit(txt, (x, y))
                if r == 2:
                    "Action text"
                    if self.action:
                        y = row_ys[r]
                        row, col = self.board.pieceSelected[0], self.board.pieceSelected[1]
                        if self.action == 'move':
                            txt = self.menu_font.render(f"Click on the board to move "
                                                        f"(speed={self.board.board[row][col]})", False, font_color)
                        elif self.action == 'basic':
                            txt = self.menu_font.render(f"Click the target for action: "
                                                        f"{self.board.board[row][col].basic['name']}", False, font_color)
                        elif self.action == 'special':
                            txt = self.menu_font.render(f"Click the target for action: "
                                                        f"{self.board.board[row][col].special['name']}", False, font_color)
                        elif self.action == 'utility':
                            txt = self.menu_font.render(f"Click the target for action: "
                                                        f"{self.board.board[row][col].utility['name']}", False, font_color)
                        self.win.blit(txt, (x, y))
            elif self.menu_state == 'abilities':
                # Abilities menu shows selected piece's abilities, and a back button to return to main menu
                x = 10
                x_title, y_title = x + 80, lambda r_y: r_y - 20
                y_line1, y_line2 = lambda r_y: r_y + 30, lambda r_y: r_y + 60
                if r == 0:
                    "Back button"
                    txt = self.menu_font.render("BACK", False, font_color)
                    y = row_ys[r]
                    self.win.blit(txt, (x, y))
                if self.board.pieceSelected:
                    row, col = self.board.pieceSelected[0], self.board.pieceSelected[1]
                    if r == 1:
                        "Basic ability"
                        txt = self.menu_font.render(f"{self.board.board[row][col].basic['name']}", False, font_color)
                        y = row_ys[r]
                        title_txt = self.menu_font.render("--BASIC--", False, font_color)
                        self.win.blit(title_txt, (x_title+8, y_title(y)))
                        txt1 = self.menu_font.render(f"damage: {self.board.board[row][col].basic['damage']},  "
                                                     f"range: {self.board.board[row][col].basic['range']},  "
                                                     f"c/d: {self.board.board[row][col].basic['cd']}", False, font_color)
                        txt2 = self.menu_font.render(f"{self.board.board[row][col].basic['info']}", False, font_color)
                        self.win.blit(txt1, (x, y_line1(y)))
                        self.win.blit(txt2, (x, y_line2(y)))
                    elif r == 2:
                        "Special ability"
                        txt = self.menu_font.render(f"{self.board.board[row][col].special['name']}", False, font_color)
                        y = row_ys[r]
                        title_txt = self.menu_font.render("--SPECIAL--", False, font_color)
                        self.win.blit(title_txt, (x_title-6, y_title(y)))
                        txt1 = self.menu_font.render(f"damage: {self.board.board[row][col].special['damage']},  "
                                                     f"range: {self.board.board[row][col].special['range']},  "
                                                     f"c/d: {self.board.board[row][col].special['cd']}", False, font_color)
                        txt2 = self.menu_font.render(f"{self.board.board[row][col].special['info']}", False, font_color)
                        self.win.blit(txt1, (x, y_line1(y)))
                        self.win.blit(txt2, (x, y_line2(y)))
                    elif r == 3:
                        "Utility ability"
                        txt = self.menu_font.render(f"{self.board.board[row][col].utility['name']}", False, font_color)
                        y = row_ys[r]
                        title_txt = self.menu_font.render("--UTILITY--", False, font_color)
                        self.win.blit(title_txt, (x_title, y_title(y)))
                        txt1 = self.menu_font.render(f"damage: {self.board.board[row][col].utility['damage']},  "
                                                     f"range: {self.board.board[row][col].utility['range']},  "
                                                     f"c/d: {self.board.board[row][col].utility['cd']}", False, font_color)
                        txt2 = self.menu_font.render(f"{self.board.board[row][col].utility['info']}", False, font_color)
                        self.win.blit(txt1, (x, y_line1(y)))
                        self.win.blit(txt2, (x, y_line2(y)))
                    self.win.blit(txt, (x, y))

    def draw_menus(self, pos):
        border_color = (100, 55, 10)   # brown
        menu_color = (20, 25, 25)     # gray
        font_color = (255, 255, 255)  # white
        alpha = 50
        border = 5

        menu = self.draw_rect(self.MENU_WIDTH-border*2, self.MENU_HEIGHT-border*2, border, menu_color, border_color)
        self.win.blit(menu, (self.MENU_X, self.MENU_Y))
        self.menu_text(font_color)

        top_menu = self.draw_rect(self.MENU_WIDTH-border*2, self.TOP_MENU_HEIGHT-border*2, border, (0,0,0), border_color)
        self.win.blit(top_menu, (0, 0))
        self.top_menu_text(font_color)

        # TODO: finish implementing menu hover graphic
        # if pos[0] < self.BOARD_X and pos[1] > self.MENU_Y:
        #     menu_row = self.check_menu_hover(pos)
        #     self.draw_aura('rect', 'menu', menu_row)

    def draw(self, pos):
        """Draws game board and menus onto screen with each frame (rate set by self.FPS)"""
        self.board.draw(self.win, self.action)
        self.draw_menus(pos)
        pygame.display.update()

    def end_turn(self):
        self.menu_state = 'main'
        self.action = 'idle'
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

            pos = pygame.mouse.get_pos()
            self.draw(pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if pygame.mouse.get_pressed()[0]:
                    if pos[0] < self.BOARD_X:
                        # Player clicked outside game board
                        self.click(pos)
                    else:
                        # Player clicked inside game board
                        turn = self.board.click(pos, self.turn, self.action)
                        if turn != self.turn:
                            self.end_turn()

        pygame.quit()


if __name__ == '__main__':
    pygame.font.init()
    g = Game()
    g.run()
