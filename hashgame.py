import pygame
import sys
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def xy_to_ij(x, y):
    '''
    i - column index
    j - row index
    '''
    i = 0 if x <= 100 else 1 if x <= 200 else 2
    j = 0 if y <= 100 else 1 if y <= 200 else 2
    return i, j

def copy_state(state):
    return [[cell for cell in col] for col in state]

def check_vertical_winner(state):
    for i in range(3):
        for player in ['x', 'o']:
            if state[i][0] == player and state[i][1] == player and state[i][2] == player:
                return player, i
    return None, None

def check_horizontal_winner(state):
    for j in range(3):
        for player in ['x', 'o']:
            if state[0][j] == player and state[1][j] == player and state[2][j] == player:
                return player, j
    return None, None

def check_diagonal_winner(state):
    for player in ['x', 'o']:
        if state[0][0] == player and state[1][1] == player and state[2][2] == player:
            return player, True #main diagonal
        if state[2][0] == player and state[1][1] == player and state[0][2] == player:
            return player, False #secondary diagonal
    return None, None

def state_full(state):
    '''
    Returns True if there is no empty spaces in the state
    '''
    for i in range(3):
        for j in range(3):
            if state[i][j] == '_':
                return False
    return True

def who_win(state):
    '''
    Returns the winner player for the state
    '''
    wp, wi = check_vertical_winner(state)
    if wp != None:
        return wp

    wp, wj = check_horizontal_winner(state)
    if wp != None:
        return wp

    wp, wmain = check_diagonal_winner(state)
    if wp != None:
        return wp

    return None

class HashGameGUI():
    def __init__(self):
        self.display = None
        self.state = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        self.player = 'x'
        self.end = False

    def draw_grid(self):
        #vertical lines
        pygame.draw.line(self.display, WHITE, (100, 0), (100, 300), 4)
        pygame.draw.line(self.display, WHITE, (200, 0), (200, 300), 4)
        #horizontal lines
        pygame.draw.line(self.display, WHITE, (0, 100), (300, 100), 4)
        pygame.draw.line(self.display, WHITE, (0, 200), (300, 200), 4)

    def draw_x(self, i, j):
        pygame.draw.line(self.display, GREEN, (100*i, 100*j), (100*(i+1), 100*(j+1)), 4)
        pygame.draw.line(self.display, GREEN, (100*(i+1), 100*j), (100*(i), 100*(j+1)), 4)

    def draw_o(self, i, j):
        pygame.draw.circle(self.display, GREEN, (100*(i+0.5), 100*(j+0.5)), 45, 4)

    def draw_vertical_line(self, i):
        pygame.draw.line(self.display, RED, (100*(i+0.5), 0), (100*(i+0.5), 300), 4)
    
    def draw_horizontal_line(self, j):
        pygame.draw.line(self.display, RED, (0, 100*(j+0.5)), (300, 100*(j+0.5)), 4)

    def draw_diagonal_line(self, main):
        if main == True:
            pygame.draw.line(self.display, RED, (0, 0), (300, 300), 4)
        else:
            pygame.draw.line(self.display, RED, (300, 0), (0, 300), 4)

    def check_and_draw_winner(self):
        wp, wi = check_vertical_winner(self.state)

        if wp != None:
            self.draw_vertical_line(wi)
            self.end = True
            print('winner:', wp)
            return

        wp, wj = check_horizontal_winner(self.state)

        if wp != None:
            self.draw_horizontal_line(wj)
            self.end = True
            print('winner:', wp)
            return

        wp, wmain = check_diagonal_winner(self.state)

        if wp != None:
            self.draw_diagonal_line(wmain)
            self.end = True
            print('winner:', wp)
            return

        if state_full(self.state):
            self.end = True
            return

    def draw_all(self):
        self.display.fill(BLACK)
        self.draw_grid()
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 'x':
                    self.draw_x(i, j)
                elif self.state[i][j] == 'o':
                    self.draw_o(i, j)
        
        self.check_and_draw_winner()

    def toggle_player(self):
        self.player = 'o' if self.player == 'x' else 'x'
        print('player:', self.player)

    def on_click(self, i, j):
        if self.end == False:
            if self.player == 'x':
                if self.state[i][j] == '_': 
                    self.state[i][j] = 'x' #change state
                    self.toggle_player()
            elif self.player == 'o':
                if self.state[i][j] == '_': 
                    self.state[i][j] = 'o' #change state
                    self.toggle_player()

    def show(self):
        pygame.init()
        self.display = pygame.display.set_mode((300, 300))
        pygame.display.set_caption('Hash Game')
        self.draw_all()
        print('player:', self.player)

        while True: # main game loop
            for event in pygame.event.get():
                if event.type == QUIT: #quit event
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: #click event
                    if event.button == 1: #left button
                        x, y = pygame.mouse.get_pos()
                        i, j = xy_to_ij(x, y)
                        self.on_click(i, j)
                        self.draw_all()

            pygame.display.update()

if __name__ == '__main__':
    gui = HashGameGUI()
    gui.show()