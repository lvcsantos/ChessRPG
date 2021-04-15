import pygame
import os
from piece import Cleric
from piece import Paladin
from piece import Ranger
from piece import Rogue
from piece import Wizard
from piece import Dragon


class Board:
    def __init__(self, x, y, board_len, grid_len):
        self.GRID = grid_len
        self.WIDTH = self.HEIGHT = board_len
        self.x, self.y = x, y
        self.board_img = pygame.transform.scale(pygame.image.load(os.path.join("img", "dark_grid_9x9.png")),
                                                (self.WIDTH, self.HEIGHT))

        self.board = [[0 for x in range(self.GRID)] for _ in range(self.GRID)]

        self.board[0][2] = Paladin(0, 2, 'Player 1', board_len, self.GRID, [x, y])
        self.board[0][3] = Cleric(0, 3, 'Player 1', board_len, self.GRID, [x, y])
        self.board[0][4] = Wizard(0, 4, 'Player 1', board_len, self.GRID, [x, y])
        self.board[0][5] = Rogue(0, 5, 'Player 1', board_len, self.GRID, [x, y])
        self.board[0][6] = Ranger(0, 6, 'Player 1', board_len, self.GRID, [x, y])

        self.board[8][2] = Paladin(8, 2, 'Player 2', board_len, self.GRID, [x, y])
        self.board[8][3] = Cleric(8, 3, 'Player 2', board_len, self.GRID, [x, y])
        self.board[8][4] = Wizard(8, 4, 'Player 2', board_len, self.GRID, [x, y])
        self.board[8][5] = Rogue(8, 5, 'Player 2', board_len, self.GRID, [x, y])
        self.board[8][6] = Ranger(8, 6, 'Player 2', board_len, self.GRID, [x, y])

        # self.board[4][4] = Dragon(4, 4, 'Wild', board_len, self.GRID, [x, y])

        self.pieceSelected = False
        self.winner = None

    def draw(self, win, action):
        win.blit(self.board_img, (self.x, self.y))
        for r in range(self.GRID):
            for c in range(self.GRID):
                if self.board[r][c] != 0:
                    self.board[r][c].draw(win, self.board, action)

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

    def aoe_damage(self, aoe_len, damage, row, col):
        for r in range(aoe_len):
            aoe_row = row + (r - 1)
            if 0 <= aoe_row < self.GRID:
                for c in range(aoe_len):
                    aoe_col = col + (c - 1)
                    if 0 <= aoe_col <= self.GRID:
                        if self.board[aoe_row][aoe_col] != 0:
                            self.board[aoe_row][aoe_col].hp = self.board[aoe_row][aoe_col].hp - damage

    def click(self, pos, turn, action):
        row = int(((pos[1] - self.y) / self.HEIGHT) * self.GRID)
        col = int(((pos[0] - self.x) / self.WIDTH) * self.GRID)

        if 0 <= row <= self.GRID and 0 <= col <= self.GRID:
            # player clicked inside the board
            if self.board[row][col] != 0:
                # there is a piece in this tile
                if not self.board[row][col].selected and self.board[row][col].player == turn:
                    # this piece is not selected and belongs to current player
                    if action == 'idle':
                        # not an action, so select it
                        self.board[row][col].selected = True
                        if self.pieceSelected:
                            # another piece was previously selected, so unselect it
                            old_row, old_col = self.pieceSelected
                            self.unselect(old_row, old_col)
                        self.pieceSelected = (row, col)
                    elif action == 'special':
                        # special action by another selected piece
                        sel_row, sel_col = self.pieceSelected
                        if isinstance(self.board[sel_row][sel_col], Cleric):
                            # Heal ability by a Cleric piece on ally, execute and end turn
                            self.board[row][col].hp = self.board[row][col].hp + self.board[sel_row][sel_col].special['damage']
                            turn = self.end_turn(turn, sel_row, sel_col)
                elif not self.board[row][col].selected and self.board[row][col].player != turn:
                    # this piece is not selected and does not belong to current player
                    if self.pieceSelected:
                        sel_row, sel_col = self.pieceSelected
                    if action == 'basic':
                        # basic action by another selected piece
                        self.board[row][col].hp = self.board[row][col].hp - self.board[sel_row][sel_col].basic['damage']
                        turn = self.end_turn(turn, sel_row, sel_col)
                    elif action == 'special':
                        # special action by another selected piece
                        damage = self.board[sel_row][sel_col].special['damage']
                        if isinstance(self.board[sel_row][sel_col], Wizard):
                            # Fireball ability by a Wizard
                            self.aoe_damage(3, damage, row, col)
                        elif isinstance(self.board[sel_row][sel_col], Ranger):
                            # Thorns ability by a Ranger
                            # TODO: implement thorns condition in grid tiles
                            self.aoe_damage(3, damage, row, col)
                        else:
                            self.board[row][col].hp = self.board[row][col].hp - damage
                        turn = self.end_turn(turn, sel_row, sel_col)
                    elif action == 'utility':
                        damage = self.board[sel_row][sel_col].utility['damage']
                        # if isinstance(self.board[sel_row][sel_col], Cleric):
                        #     # Fear ability by a Cleric
                        #     # TODO:
                        #     pass
                        # elif isinstance(self.board[sel_row][sel_col], Ranger):
                        #     # Entangle ability by a Ranger
                        #     # TODO:
                        #     pass
                        # else:
                        self.board[row][col].hp = self.board[row][col].hp - damage
                        turn = self.end_turn(turn, sel_row, sel_col)
                elif self.board[row][col].selected and self.board[row][col].player == turn:
                    # this piece is already selected and belongs to current player
                    if action == 'idle':
                        # not an action, so unselect it
                        self.unselect(row, col)
                    elif action == 'special' and isinstance(self.board[row][col], Cleric):
                        # Heal ability by a Cleric piece on self, execute and end turn
                        self.board[row][col].hp = self.board[row][col].hp + self.board[row][col].special['damage']
                        turn = self.end_turn(turn, row, col)
            else:
                # this tile is empty
                if self.pieceSelected:
                    # a piece is selected
                    sel_row, sel_col = self.pieceSelected
                    if action == 'move':
                        # move action, so move piece to tile if the move is valid and end turn
                        if self.board[sel_row][sel_col].is_move_valid(self.board, row, col):
                            self.move_piece(sel_row, sel_col, row, col)
                            turn = self.end_turn(turn, row, col)
                    elif action == 'basic':
                        if isinstance(self.board[self.pieceSelected[0]][self.pieceSelected[1]], Paladin):
                            # Smash ability by a Paladin piece, move target to this square if valid
                            # TODO:
                            turn = self.end_turn(turn, sel_row, sel_col)
                    elif action == 'special':
                        damage = self.board[sel_row][sel_col].special['damage']
                        if isinstance(self.board[sel_row][sel_col], Ranger):
                            # Thorns ability by a Ranger
                            # TODO: implement thorns condition in grid tiles
                            self.aoe_damage(3, damage, row, col)
                        elif isinstance(self.board[sel_row][sel_col], Wizard):
                            # Fireball ability by a Wizard
                            self.aoe_damage(3, damage, row, col)
                        turn = self.end_turn(turn, sel_row, sel_col)
                    elif action == 'utility':
                        if isinstance(self.board[sel_row][sel_col], Wizard):
                            # Blink ability by a Wizard
                            # TODO: implement cooldown, check if blink move valid
                            self.move_piece(sel_row, sel_col, row, col)
                            turn = self.end_turn(turn, row, col)

        return turn

    def move_piece(self, old_row, old_col, new_row, new_col):
        self.board[old_row][old_col].change_loc(new_row, new_col)
        self.board[new_row][new_col] = self.board[old_row][old_col]
        self.board[old_row][old_col] = 0
        self.pieceSelected = False

    def reset(self, win):
        win.blit(self.board_img, (self.x, self.y))

