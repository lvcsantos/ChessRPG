import pygame
import os

frame = 0


class Piece:
    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        self.SIZE = int(board_len / 10)
        self.Y_OFFSET = 6
        self.TILE_SIZE = board_len / grid_len
        self.GRID = grid_len
        self.BOARD_X = board_xy[0]
        self.BOARD_Y = board_xy[1]
        self.row = row
        self.col = col
        self.player = player
        self.speed = 0
        self.selected = False
        self.move_list = []
        self.sel_img = pygame.image.load(os.path.join('img', 'selected_aura.png'))

    def change_loc(self, new_row, new_col):
        self.row = new_row
        self.col = new_col

    def grid2pos(self, row, col, offset=True):
        if offset:
            y = row * self.TILE_SIZE + self.Y_OFFSET + self.BOARD_Y
        else:
            y = row * self.TILE_SIZE + self.BOARD_Y
        x = col * self.TILE_SIZE + self.BOARD_X
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
        elif mode == 'ability':
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

    def draw(self, win, board, action):
        if self.hp > 0:
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
            if action == 'move':
                moves = self.get_moves(board, mode='move')
                surf = pygame.Surface((tile_size, tile_size))
                surf.set_alpha(alpha)
                pygame.draw.rect(surf, tile_color, rect)
                for move in moves:
                    win.blit(surf, self.grid2pos(move[0], move[1], offset=False))


class Dragon(Piece):
    """
        Abilities

    """

    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        super().__init__(row, col, player, board_len, grid_len, board_xy)
        self.SIZE = int(self.TILE_SIZE * 2)
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
            self.color = 'gold'
        else:
            self.color = 'gold'
        img = pygame.image.load(os.path.join('img', f'dragon_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))


class Wizard(Piece):
    """
        Abilities
        Fire Bolt: Range=5 | Damage=5 | CD=0 | Description=Hurl fire at one target to deal 5 damage
        Fireball: Range=4 | Damage=4 | CD=0 | Description=Deals 4 damage per target in a 3x3 square
        Blink: Range=5 | Damage=0 | CD=1 | Description=Can teleport five tiles (doesn't count as move action)
    """

    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        super().__init__(row, col, player, board_len, grid_len, board_xy)
        self.name = 'Wizard'
        self.y_offset = 4
        self.hp = 13
        self.speed = 1
        self.abilities = {'basic': 'Firebolt', 'special': 'Fireball', 'utility': 'Blink'}
        self.basic = {'name': 'Firebolt', 'damage': 5, 'range': 5, 'cd': 0, 'info': 'Hurl a bolt of fire at a foe'}
        self.special = {'name': 'Fireball', 'damage': 3, 'range': 4, 'cd': 0, 'info': 'Throw a ball of fire (3x3 area)'}
        self.utility = {'name': 'Blink', 'damage': 0, 'range': 5, 'cd': 0, 'info': 'Teleport to target location'}

        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'wizard_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))


class Rogue(Piece):
    """
        Abilities
        Stab: Range=1 | Damage=4 | CD=0 | Description=Stab a target from any direction
        Backstab: Range=1 | Damage=6 | CD=1 | Description=Stab a target from the back
        Hide: Range=0 | Damage=0 | CD=1 | Description=Can't be targeted with damage abilities until next turn
    """

    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        super().__init__(row, col, player, board_len, grid_len, board_xy)
        self.name = 'Rogue'
        self.hp = 16
        self.speed = 5
        self.basic = {'name': 'Stab', 'damage': 4, 'range': 1, 'cd': 0, 'info': 'Stab foe with a dagger'}
        self.special = {'name': 'Backstab', 'damage': 6, 'range': 1, 'cd': 1, 'info': 'Critical stab from behind'}
        self.utility = {'name': 'Hide', 'damage': 0, 'range': 0, 'cd': 1, 'info': 'Cannot be targeted for 1 turn'}
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'rogue_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))


class Cleric(Piece):
    """
        Abilities
        Smite: Range=3 | Damage=5 | CD=0 | Description=Deals 5 damage to one target
        Heal: Range=1 | Damage=4 | CD=1 | Description=Heal self or ally on touch for 4HP
        Fear: Range=2 | Damage=0 | CD=0 | Description=Causes an enemy to run away up to 5 tiles to a chosen location
    """

    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        super().__init__(row, col, player, board_len, grid_len, board_xy)
        self.name = 'Cleric'
        self.y_offset = 10
        self.hp = 14
        self.speed = 2
        self.basic = {'name': 'Smite', 'damage': 3, 'range': 3, 'cd': 0, 'info': 'Hit foe with radiant strike'}
        self.special = {'name': 'Heal', 'damage': 4, 'range': 1, 'cd': 1, 'info': 'Heal an ally or self'}
        self.utility = {'name': 'Fear', 'damage': 2, 'range': 3, 'cd': 0, 'info': 'Enemy runs away up to 5 tiles'}
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'cleric_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))


class Paladin(Piece):
    """
        Abilities
        Smash: Range=1 | Damage=4 | CD=0 | Description=Smash a target to deal 4 damage and move up to 2 squares
        Stun: Range=1 | Damage=1 | CD=1 | Description=Cause a target to lose all actions for 1 turn
        Dispel: Range=2 | Damage=0 | CD=1 | Description=Choose one ability for the target to lose for 2 turns
    """

    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        super().__init__(row, col, player, board_len, grid_len, board_xy)
        self.name = 'Paladin'
        self.y_offset = 10
        self.hp = 16
        self.speed = 3
        self.basic = {'name': 'Smash', 'damage': 4, 'range': 1, 'cd': 0, 'info': 'Strike & move target 2 tiles'}
        self.special = {'name': 'Stun', 'damage': 2, 'range': 1, 'cd': 1, 'info': 'Stun an enemy for 1 turn'}
        self.utility = {'name': 'Dispel', 'damage': 2, 'range': 3, 'cd': 0, 'info': 'Block target ability for 2 turns'}
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'paladin_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))


class Ranger(Piece):
    """
        Abilities
        Bow: Range=5 | Damage=4 | CD=0 | Description=Shoot an arrow at a target to deal 4 damage
        Thorns: Range=2 | Damage=4 | CD=0 | Description=Creates a 2x2 area of thorns, deals 4 damage on enter or start,
                removed if cast again or as a bonus action
        Entangle: Range=4 | Damage=0 | CD=0 | Description=Causes a target to lose movement for 1 turn (prevents blink)
    """

    def __init__(self, row, col, player, board_len, grid_len, board_xy):
        super().__init__(row, col, player, board_len, grid_len, board_xy)
        self.name = 'Ranger'
        self.y_offset = 8
        self.hp = 16
        self.speed = 3
        self.basic = {'name': 'Arrow', 'damage': 4, 'range': 5, 'cd': 0, 'info': 'Shoot an arrow at a foe'}
        self.special = {'name': 'Thorns', 'damage': 4, 'range': 2, 'cd': 0, 'info': 'Create 2x2 area of thorns'}
        self.utility = {'name': 'Entangle', 'damage': 2, 'range': 4, 'cd': 1, 'info': 'Target loses move for 2 turns'}
        if self.player == 'Player 1':
            self.color = 'red'
        else:
            self.color = 'blue'
        img = pygame.image.load(os.path.join('img', f'ranger_{self.color}.png'))
        self.img = pygame.transform.scale(img, (self.SIZE, self.SIZE))
