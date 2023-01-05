'''
This is a tic-tac-toe program with a GUI as well as a bot which runs through an algorithm which you can play against.
This program makes use of OOP
'''

import pygame
import random
import os

pygame.init()

monitorInfo = pygame.display.Info()
x = monitorInfo.current_w / 2 - 450
y = monitorInfo.current_h / 2 - 500
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

screen = pygame.display.set_mode((900, 1000))
pygame.display.set_caption('Tic Tac Toe')
black = (0, 0, 0)

board = ['-', '-', '-',
         '-', '-', '-',
         '-', '-', '-']

playeroptions = ['X', 'O']
moves = 0

outcome1 = [0, 3, 6, 0, 1, 2, 0, 2]
outcome2 = [1, 4, 7, 3, 4, 5, 4, 4]
outcome3 = [2, 5, 8, 6, 7, 8, 8, 6]

boardnum = [0, 1, 2, 3, 4, 5, 6, 7, 8]
rowval = [0, 1, 2, 0, 1, 2, 0, 1, 2]
colval = [0, 0, 0, 1, 1, 1, 2, 2, 2]

gamefont = pygame.font.SysFont('comicsans', 500)
text2 = pygame.font.SysFont('comicsans', 100)
text3 = pygame.font.SysFont('comicsans', 75)
text4 = pygame.font.SysFont('comicsans', 150)

X = gamefont.render('X', True, black)
O = gamefont.render('O', True, black)

wintextX = text2.render('X wins', True, black)
wintextO = text2.render('O wins', True, black)
wintexttie = text2.render('Tie', True, black)
playagain = text3.render('Play Again', True, (29, 42, 181))
title = text2.render('Welcome to', True, black)
title2 = text4.render('Tic-Tac-Toe!', True, black)
playtext = text2.render('Play', True, (29, 42, 181))
backtext = text3.render('<= Back', True, (29, 42, 181))
undertitle = text2.render('vs Defence Bot', True, black)
stattext = text2.render('Stats', True, (29, 42, 181))
stattitle = text2.render('Statistics', True, black)

status = 'play'
winner = 'none'
currentscreen = 'title'

xwins = 0
owins = 0
tiecount = 0

Xwins = text3.render('X Wins(you):', True, black)
Owins = text3.render('O Wins(bot):', True, black)
tienum = text3.render('Number of ties:', True, black)


class grid:

    def __init__(self):
        self.grid_lines = [((0, 300), (900, 300)),
                           ((0, 600), (900, 600)),
                           ((0, 900), (900, 900)),
                           ((300, 0), (300, 900)),
                           ((600, 0), (600, 900))]

    def draw(self):
        for line in self.grid_lines:
            pygame.draw.line(screen, black, line[0], line[1], 5)


class buttons:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def drawbutton(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


backbutton = buttons((66, 149, 245), 20, 920, 240, 60)
playbutton = buttons((66, 149, 245), 320, 650, 260, 100)
statbutton = buttons((66, 149, 245), 320, 800, 260, 100)
playagainbutton = buttons((66, 149, 245), 600, 920, 280, 60)

Grid = grid()


def check_win():
    global status
    global xwins, owins

    for i in playeroptions:
        for outcome_1, outcome_2, outcome_3 in zip(outcome1, outcome2, outcome3):
            if board[outcome_1] == i and board[outcome_2] == i and board[outcome_3] == i:
                global winner
                winner = i
                status = 'finished'
                break

    if winner == 'X':
        xwins += 1
    if winner == 'O':
        owins += 1


def ai_algorithm():
    condition = 'not currently winning'
    condition2 = 'o not winning'
    spots = 'any'

    corners = [0, 2, 6, 8]
    edges = [1, 3, 5, 7]
    outcome4 = [1, 1, 5, 7]
    outcome5 = [3, 5, 7, 3]
    ocorner = [4, 4, 4, 4]
    placement = [0, 2, 8, 6]

    cornerx = [0, 2, 8, 6]
    middlex = [4, 4, 4, 4]
    cornero = [8, 6, 0, 2]
    choosespots = [2, 8, 2, 8]

    for j in range(len(board)):

        if board[j] == '-':
            board[j] = 'O'
            for outcome_1, outcome_2, outcome_3 in zip(outcome1, outcome2, outcome3):
                if board[outcome_1] == 'O' and board[outcome_2] == 'O' and board[outcome_3] == 'O':
                    condition2 = 'can win'

            if condition2 == 'can win':
                board[j] = 'O'
                break
            else:
                board[j] = '-'

    if condition2 == 'o not winning':
        for j in range(len(board)):
            if board[j] == '-':
                board[j] = 'X'

                for outcome_1, outcome_2, outcome_3 in zip(outcome1, outcome2, outcome3):
                    if board[outcome_1] == 'X' and board[outcome_2] == 'X' and board[outcome_3] == 'X':
                        condition = 'can win'

                if condition == 'not currently winning':
                    board[j] = '-'

                if condition == 'can win':
                    board[j] = 'O'
                    break

    if condition == 'not currently winning' and condition2 == 'o not winning':

        if moves == 1:

            if board[4] == 'X':
                ai_choice = random.choice(corners)
                spots = 'specific'

            for i in corners:
                if board[i] == 'X':
                    ai_choice = 4
                    spots = 'specific'

            for j in edges:
                if board[j] == 'X':
                    ai_choice = 4
                    spots = 'specific'

        if moves == 3:

            for a, b, c, d in zip(outcome4, outcome5, ocorner, placement):
                if board[a] == 'X' and board[b] == 'X' and board[c] == 'O':
                    ai_choice = d
                    spots = 'specific'
                    break

            if board[0] == 'X' and board[8] == 'X' and board[4] == 'O':
                ai_choice = random.choice(edges)
                spots = 'specific'

            if board[2] == 'X' and board[6] == 'X' and board[4] == 'O':
                ai_choice = random.choice(edges)
                spots = 'specific'

            if board[3] == 'X' and board[5] == 'X' and board[4] == 'O':
                ai_choice = random.choice(corners)
                spots = 'specific'

            if board[1] == 'X' and board[7] == 'X' and board[4] == 'O':
                ai_choice = random.choice(corners)
                spots = 'specific'

            for a, b, c, d in zip(cornerx, middlex, cornero, choosespots):
                if board[a] == 'X' and board[b] == 'X' and board[c] == 'O':
                    ai_choice = d
                    spots = 'specific'

        if spots == 'any':
            if moves != 1:
                ai_choice = random.randint(0, 8)
                while board[ai_choice] != '-':
                    ai_choice = random.randint(0, 8)

        board[ai_choice] = 'O'


def draw():
    if currentscreen == 'title':
        screen.fill((166, 173, 255))

        pygame.draw.rect(screen, (255, 255, 255), [125, 130, 650, 300])
        pygame.draw.rect(screen, black, [125, 130, 650, 300], 5)

        screen.blit(title, (250, 160))
        screen.blit(title2, (160, 220))
        screen.blit(undertitle, (205, 310))

        playbutton.drawbutton()
        pygame.draw.rect(screen, (29, 42, 181), [320, 650, 260, 100], 5)
        screen.blit(playtext, (380, 665))

        statbutton.drawbutton()
        pygame.draw.rect(screen, (29, 42, 181), [320, 800, 260, 100], 5)
        screen.blit(stattext, (370, 815))

    if currentscreen == 'gamescreen':
        screen.fill((255, 255, 255))
        Grid.draw()

        backbutton.drawbutton()
        pygame.draw.rect(screen, (29, 42, 181), [20, 920, 240, 60], 5)
        screen.blit(backtext, (35, 925))

        for a, b, c in zip(boardnum, rowval, colval):
            if board[a] == 'X':
                screen.blit(X, (40 + (300 * b), 0 + (300 * c)))
            if board[a] == 'O':
                screen.blit(O, (20 + (300 * b), 0 + (300 * c)))

        if status == 'finished':
            if winner == 'X':
                screen.blit(wintextX, (330, 920))
            if winner == 'O':
                screen.blit(wintextO, (330, 920))
            if winner == 'tie':
                screen.blit(wintexttie, (390, 920))

            playagainbutton.drawbutton()
            pygame.draw.rect(screen, (29, 42, 181), [600, 920, 280, 60], 5)
            screen.blit(playagain, (607, 925))

    if currentscreen == 'statscreen':
        screen.fill((166, 173, 255))

        backbutton.drawbutton()
        pygame.draw.rect(screen, (29, 42, 181), [20, 920, 240, 60], 5)
        screen.blit(backtext, (35, 925))

        pygame.draw.rect(screen, (255, 255, 255), [150, 100, 600, 700])
        pygame.draw.rect(screen, black, [150, 100, 600, 700], 5)

        screen.blit(stattitle, (290, 120))
        pygame.draw.line(screen, black, (280, 185), (620, 185), 5)

        Xwinnum = text2.render(str(xwins), True, black)
        Owinnum = text2.render(str(owins), True, black)
        tienumnum = text2.render(str(tiecount), True, black)

        screen.blit(Xwins, (290, 250))
        screen.blit(Xwinnum, (430, 325))

        screen.blit(Owins, (290, 425))
        screen.blit(Owinnum, (430, 500))

        screen.blit(tienum, (260, 600))
        screen.blit(tienumnum, (430, 675))

    pygame.display.update()


turn = 'player'

run = True
while run:

    draw()

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if currentscreen == 'gamescreen' or currentscreen == 'statscreen':
                if backbutton.isOver(pos):
                    backbutton.color = (96, 166, 247)

            if currentscreen == 'title':
                if playbutton.isOver(pos):
                    playbutton.color = (96, 166, 247)

                if statbutton.isOver(pos):
                    statbutton.color = (96, 166, 247)

            if currentscreen == 'gamescreen':
                if status == 'finished':
                    if playagainbutton.isOver(pos):
                        playagainbutton.color = (96, 166, 247)

        if event.type == pygame.MOUSEBUTTONUP:
            if currentscreen == 'gamescreen':
                if backbutton.isOver(pos):
                    backbutton.color = (66, 149, 245)
                    currentscreen = 'title'
                    if status == 'finished':
                        status = 'play'
                        winner = 'none'
                        turn = 'player'
                        moves = 0
                        for i in range(9):
                            board[i] = '-'

                if status == 'play':

                    startx = [0, 0, 0, 300, 300, 300, 600, 600, 600]
                    endx = [300, 300, 300, 600, 600, 600, 900, 900, 900]
                    starty = [0, 300, 600, 0, 300, 600, 0, 300, 600]
                    endy = [300, 600, 900, 300, 600, 900, 300, 600, 900]
                    boardspots = [0, 3, 6, 1, 4, 7, 2, 5, 8]

                    for a, b, c, d, e in zip(startx, endx, starty, endy, boardspots):
                        if a <= pos[0] <= b:
                            if c <= pos[1] <= d:
                                if board[e] == '-':
                                    board[e] = 'X'
                                    turn = 'ai'
                                    moves += 1

                if status == 'finished':
                    if playagainbutton.isOver(pos):
                        playagainbutton.color = (66, 149, 245)
                        status = 'play'
                        winner = 'none'
                        turn = 'player'
                        moves = 0
                        for i in range(9):
                            board[i] = '-'

            if currentscreen == 'title':
                if playbutton.isOver(pos):
                    playbutton.color = (66, 149, 245)
                    currentscreen = 'gamescreen'

                if statbutton.isOver(pos):
                    statbutton.color = (66, 149, 245)
                    currentscreen = 'statscreen'

            if currentscreen == 'statscreen':
                if backbutton.isOver(pos):
                    backbutton.color = (66, 149, 245)
                    currentscreen = 'title'

    if status == 'play':
        check_win()

    if status == 'play':
        if '-' not in board:
            status = 'finished'
            winner = 'tie'
            tiecount += 1

    if turn == 'ai' and status == 'play':
        ai_algorithm()
        moves += 1
        turn = 'player'
        check_win()
