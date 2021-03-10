import pygame
import os
from piece import Cleric
from piece import Paladin
from piece import Ranger
from piece import Rogue
from piece import Wizard


class Board:
    def __init__(self, x, y, width, height):
        self.GRID = 9
        self.WIDTH, self.HEIGHT = width, height
        self.x, self.y = x, y
        self.board_img = pygame.transform.scale(pygame.image.load(os.path.join("img", "dark_grid_9x9.png")),
                                                (self.WIDTH, self.HEIGHT))

        self.board = [[0 for x in range(self.GRID)] for _ in range(self.GRID)]

        self.board[0][2] = Paladin(0, 2, 'Player 1', self.WIDTH, self.GRID)
        self.board[0][3] = Cleric(0, 3, 'Player 1', self.WIDTH, self.GRID)
        self.board[0][4] = Wizard(0, 4, 'Player 1', self.WIDTH, self.GRID)
        self.board[0][5] = Rogue(0, 5, 'Player 1', self.WIDTH, self.GRID)
        self.board[0][6] = Ranger(0, 6, 'Player 1', self.WIDTH, self.GRID)

        self.board[8][2] = Paladin(8, 2, 'Player 2', self.WIDTH, self.GRID)
        self.board[8][3] = Cleric(8, 3, 'Player 2', self.WIDTH, self.GRID)
        self.board[8][4] = Wizard(8, 4, 'Player 2', self.WIDTH, self.GRID)
        self.board[8][5] = Rogue(8, 5, 'Player 2', self.WIDTH, self.GRID)
        self.board[8][6] = Ranger(8, 6, 'Player 2', self.WIDTH, self.GRID)

        self.pieceSelected = False
        self.winner = None

    def draw(self, win):
        win.blit(self.board_img, (self.x, self.y))
        for r in range(self.GRID):
            for c in range(self.GRID):
                if self.board[r][c] != 0:
                    self.board[r][c].draw(win, self.board)

    def unselect(self, row, col):
        self.board[row][col].selected = False
        self.pieceSelected = False

    def end_turn(self, turn, row, col):
        if turn == 'Player 1':
            turn = 'Player 2'
        else:
            turn = 'Player 1'
        self.unselect(row, col)
        return turn

    def click(self, pos, turn):
        row = int(((pos[1] - self.y) / self.HEIGHT) * self.GRID)
        col = int(((pos[0] - self.x) / self.WIDTH) * self.GRID)

        if 0 <= row <= self.GRID and 0 <= col <= self.GRID:
            # player clicked inside the board
            if self.board[row][col] != 0:
                # there is a piece in this tile
                if not self.board[row][col].selected and self.board[row][col].player == turn:
                    # this piece is not selected and belongs to current player, so select it
                    self.board[row][col].selected = True
                    if self.pieceSelected:
                        # another piece was previously selected, so unselect it
                        old_row, old_col = self.pieceSelected
                        self.unselect(old_row, old_col)
                    self.pieceSelected = (row, col)

                elif self.board[row][col].selected and self.board[row][col].player == turn:
                    # this piece is already selected and belongs to current player, so unselect it
                    self.unselect(row, col)

            else:
                # this tile is empty
                if self.pieceSelected:
                    # a piece is selected, so move it to tile if the move is valid and end turn
                    old_row, old_col = self.pieceSelected
                    if self.board[old_row][old_col].is_move_valid(self.board, row, col):
                        self.update(old_row, old_col, row, col)
                        turn = self.end_turn(turn, row, col)
        return turn

    def update(self, old_row, old_col, new_row, new_col):
        self.board[old_row][old_col].change_loc(new_row, new_col)
        self.board[new_row][new_col] = self.board[old_row][old_col]
        self.board[old_row][old_col] = 0
        self.pieceSelected = False

    def reset(self, win):
        win.blit(self.board_img, (self.x, self.y))

