import pygame
import os

frame = 0


class Piece:
    def __init__(self, row, col, player, board_size, grid_size):
        self.row = row
        self.col = col
        self.player = player
        self.speed = 0
        self.selected = False
        self.move_list = []
        self.SIZE = int(board_size / 10)
        self.y_offset = 6
        self.TILE_SIZE = board_size / grid_size
        self.GRID = grid_size
        self.sel_img = pygame.image.load(os.path.join('img', 'selected_aura.png'))

    def change_loc(self, new_row, new_col):
        self.row = new_row
        self.col = new_col

    def grid2pos(self, row, col, offset=True):
        if offset:
            y = row * self.TILE_SIZE + self.y_offset
        else:
            y = row * self.TILE_SIZE
        x = col * self.TILE_SIZE
        return x, y

    def is_move_valid(self, board, row, col):
        valid_moves = self.get_moves(board)
        if (row, col) in valid_moves:
            return True
        else:
            return False

    def get_moves(self, board, mode='move'):
        """Return list of valid tiles for movement or ability, based on mode"""
        valid_moves = []
        if mode == 'move':
            delta = self.speed
            dist = lambda row, col: abs(row - self.row) + abs(col - self.col)
        else:
            delta = self.sel_ability(mode, 'range')
            dist = lambda row, col: abs(row - self.row) + abs(col - self.col)

        for r in range(max(0, self.row - delta), min(self.GRID, self.row + delta + 1)):
            for c in range(max(0, self.col - delta), min(self.GRID, self.col + delta + 1)):
                if mode == 'move':
                    if dist(r, c) <= delta and board[r][c] == 0:
                        valid_moves.append((r, c))
                elif mode == 'ability':
                    if dist(r, c) <= delta and board[r][c] != 0:
                        valid_moves.append((r, c))
        return valid_moves

    def sel_ability(self, ability, stat=None):
        if stat:
            return self.abilities[ability][stat]

    def draw(self, win, board):
        x, y = self.grid2pos(self.row, self.col)
        win.blit(self.img, (x, y))

        # Highlight piece if current player has selected it
        if self.selected:
            aura_color = (100, 255, 100)
            tile_color = (255, 100, 0)
            tile_offset = 2
            tile_size = self.TILE_SIZE + tile_offset
            alpha = 50
            center = ((self.TILE_SIZE / 2), (self.TILE_SIZE / 2))
            radius, width = 40, 0
            rect = pygame.Rect(0, 0, tile_size, tile_size)

            sel_aura = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
            pygame.draw.circle(sel_aura, aura_color, center, radius, width)
            sel_aura.set_alpha(alpha)
            if y < 4:
                win.blit(sel_aura, (x + 1, y))
            else:
                win.blit(sel_aura, (x + 1, y - 6))
            # win.blit(pygame.transform.scale(self.sel_img, (self.SIZE+18, self.SIZE+18)), (x+2, y-16))

            # Highlight possible move or ability tiles
            # TODO: Still need to implement abilities/attacks functionality
            moves = self.get_moves(board, mode='move')
            sel_moves = pygame.Surface((tile_size, tile_size))
            sel_moves.set_alpha(alpha)
            pygame.draw.rect(sel_moves, tile_color, rect)
            for move in moves:
                win.blit(sel_moves, self.grid2pos(move[0], move[1], offset=False))


class Dragon(Piece):
    """
        Abilities
        Fire Bolt: Range=5 | Damage=5 | CD=0 | Description=Hurl fire at one target to deal 5 damage
        Fireball: Range=4 | Damage=4 | CD=0 | Description=Deals 4 damage per target in a 3x3 square
        Blink: Range=5 | Damage=0 | CD=1 | Description=Can teleport five squares (doesn't count as move action)
    """

    def __init__(self, row, col, player, board_size, grid_size):
        super().__init__(row, col, player, board_size, grid_size)
        self.y_offset = 4
        self.hp = 17
        self.speed = 4
        self.abilities = {'basic': 'Claw', 'special': 'Flame Typhoon', 'utility': 'Aerial Maneuvers'}
        self.basic = {'name': 'Claw', 'damage': 3, 'range': 1, 'cd': 0, 'info': 'Slash claws at a single foe'}
        self.special = {'name': 'Flame Typhoon', 'damage': 4, 'range': 4, 'cd': 1, 'info': 'Breathe a gust of fire in'
                                                                                           'a 3-tile cone for 2 turns'}
        self.utility = {'name': 'Aerial Maneuvers', 'damage': 0, 'range': 7, 'cd': 2, 'info': 'Fly away, immune to '
                                                                                              'melee attacks for 1 turn'}
        if self.player == 'Player 1':
            self.color = 'red'
        elif self.player == 'Player 2':
            self.color = 'blue'
        else:
            self.color = 'green'
        img = pygame.image.load(os.path.join('img', f'wizard_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))

    def firebolt(self):
        pass

    def fireball(self):
        pass

    def blink(self):
        pass


class Wizard(Piece):
    """
        Abilities
        Fire Bolt: Range=5 | Damage=5 | CD=0 | Description=Hurl fire at one target to deal 5 damage
        Fireball: Range=4 | Damage=4 | CD=0 | Description=Deals 4 damage per target in a 3x3 square
        Blink: Range=5 | Damage=0 | CD=1 | Description=Can teleport five squares (doesn't count as move action)
    """

    def __init__(self, row, col, player, board_size, grid_size):
        super().__init__(row, col, player, board_size, grid_size)
        self.y_offset = 4
        self.hp = 13
        self.speed = 1
        self.abilities = {'basic': 'Firebolt', 'special': 'Fireball', 'utility': 'Blink'}
        self.basic = {'name': 'Firebolt', 'damage': 5, 'range': 5, 'cd': 0, 'info': 'Hurl a bolt of fire at a foe'}
        self.special = {'name': 'Fireball', 'damage': 3, 'range': 4, 'cd': 0, 'info': 'Hurl a bolt of fire at a foe'}
        self.utility = {'name': 'Blink', 'damage': 0, 'range': 5, 'cd': 0, 'info': 'Hurl a bolt of fire at a foe'}
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'wizard_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))

    def firebolt(self):
        pass

    def fireball(self):
        pass

    def blink(self):
        pass


class Rogue(Piece):
    """
        Abilities
        Stab: Range=1 | Damage=4 | CD=0 | Description=Stab a target from any direction
        Backstab: Range=1 | Damage=6 | CD=1 | Description=Stab a target from the back
        Hide: Range=0 | Damage=0 | CD=1 | Description=Can't be targeted with damage abilities until next turn
    """

    def __init__(self, row, col, player, board_size, grid_size):
        super().__init__(row, col, player, board_size, grid_size)
        self.hp = 16
        self.speed = 5
        self.abilities = ['Stab', 'Backstab', 'Hide']
        self.basic_attack = {'name': 'Firebolt', 'damage': 5, 'range': 5}
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'rogue_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))

    def moves(self):
        pass


class Cleric(Piece):
    """
        Abilities
        Heal: Range=1 | Damage=4 | CD=1 | Description=Heal self or ally on touch for 4HP
        Smite: Range=3 | Damage=5 | CD=0 | Description=Deals 5 damage to one target
        Fear: Range=2 | Damage=0 | CD=0 | Description=Causes an enemy to run away 1-5 squares to a chosen location
    """

    def __init__(self, row, col, player, board_size, grid_size):
        super().__init__(row, col, player, board_size, grid_size)
        self.y_offset = 10
        self.hp = 14
        self.speed = 2
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'cleric_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))

    def moves(self):
        pass


class Paladin(Piece):
    """
        Abilities
        Smash: Range=1 | Damage=4 | CD=0 | Description=Smash a target to deal 4 damage and move up to 2 squares
        Stun: Range=1 | Damage=1 | CD=1 | Description=Cause a target to lose all actions for 1 turn
        Dispel: Range=2 | Damage=0 | CD=1 | Description=Choose one ability for the target to lose for 2 turns
    """

    def __init__(self, row, col, player, board_size, grid_size):
        super().__init__(row, col, player, board_size, grid_size)
        self.y_offset = 10
        self.hp = 16
        self.speed = 3
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'paladin_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))

    def moves(self):
        pass


class Ranger(Piece):
    """
        Abilities
        Thorns: Range=2 | Damage=4 | CD=0 | Description=Creates a 2x2 area of thorns, deals 4 damage on enter or start,
                removed if cast again or as a bonus action
        Bow: Range=5 | Damage=4 | CD=0 | Description=Shoot an arrow at a target to deal 4 damage
        Entangle: Range=4 | Damage=0 | CD=0 | Description=Causes a target to lose movement for 1 turn (prevents blink)
    """

    def __init__(self, row, col, player, board_size, grid_size):
        super().__init__(row, col, player, board_size, grid_size)
        self.y_offset = 8
        self.hp = 16
        self.speed = 3
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'ranger_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))

    def moves(self):
        pass
