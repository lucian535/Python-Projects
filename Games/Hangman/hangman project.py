'''

'''
import pygame # Imports modules
import math
import random

pygame.init()

# ---------------------------------------#
# initialize global variables/constants #
# ---------------------------------------#
BLACK = (0, 0, 0)  # Sets global colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)
highlightcolor = (181, 255, 255)

btn_font = pygame.font.SysFont("arial", 20)   # Creates Fonts
guess_font = pygame.font.SysFont("monospace", 24)
clue_font = pygame.font.SysFont("monospace", 16)

win = pygame.display.set_mode((700, 480)) # Creates the window

usedletters = []  # Global cariables that will be used
mistakes = 0
currentscreen = 'menu'
status = 'none'
finished = False
playedwords = []
word = ''
clue = ''
playsound = False
goodguess = False
checkwin = False

# Creating the text
wintext = clue_font.render('You Win!!', True, BLACK)
losetext = clue_font.render('You lose :(', True, BLACK)
nowordstext = clue_font.render('Out of words, Try a different category', True, BLACK)

title = btn_font.render('HANGMAN', True, BLACK)

# Sound effects
winsound = pygame.mixer.Sound('winsound.wav')
winsound.set_volume(0.2)

losesound = pygame.mixer.Sound('losesound.wav')
losesound.set_volume(0.2)

# ---------------------------------------#
# Classes                               #
# ---------------------------------------#

# Class for creating the buttons with letters
class LetterButtons:
    def __init__(self, x, y, letter, text, used):
        self.x = x
        self.y = y
        self.letter = letter
        self.text = text
        self.color = LIGHT_BLUE
        self.outlinecolor = BLACK
        self.radius = 20
        self.used = used

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.outlinecolor, (self.x, self.y), self.radius, 2)

        text = btn_font.render(str(self.text), True, BLACK)
        win.blit(text, (self.x - 7, self.y - 11))

    def isOver(self, pos):
        x = pos[0]
        y = pos[1]

        sqx = (x - self.x) ** 2
        sqy = (y - self.y) ** 2

        if math.sqrt(sqx + sqy) < self.radius:
            return True

        return False

# Class for creating the regular buttons
class regularbuttons:
    def __init__(self, x, y, text, color, outlinecolor, width, height, category):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.outlinecolor = outlinecolor
        self.width = width
        self.height = height
        self.category = category

    def draw(self):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(win, self.outlinecolor, [self.x, self.y, self.width, self.height], 5)

        text = btn_font.render(str(self.text), True, BLACK)
        textrect = text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))

        win.blit(text, textrect)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

# Creates the instances for the buttons
Abutton, Bbutton, Cbutton, Dbutton, Ebutton, Fbutton, \
Gbutton, Hbutton, Ibutton, Jbutton, Kbutton, Lbutton, \
Mbutton, Nbutton, Obutton, Pbutton, Qbutton, Rbutton, \
Sbutton, Tbutton, Ubutton, Vbutton, Wbutton, Xbutton, \
Ybutton, Zbutton                   =                   LetterButtons(50, 50, 'a', 'A', False), LetterButtons(100, 50, 'b', 'B', False), LetterButtons(150, 50, 'c', 'C', False), LetterButtons(200, 50, 'd', 'D', False), \
                                                       LetterButtons(250, 50, 'e', 'E', False), LetterButtons(300, 50, 'f', 'F', False), LetterButtons(350, 50, 'g', 'G', False), LetterButtons(400, 50, 'h', 'H', False), \
                                                       LetterButtons(450, 50, 'i', 'I', False), LetterButtons(500, 50, 'j', 'J', False), LetterButtons(550, 50, 'k', 'K', False), LetterButtons(600, 50, 'l', 'L', False), \
                                                       LetterButtons(650, 50, 'm', 'M', False), LetterButtons(50, 100, 'n', 'N', False), LetterButtons(100, 100, 'o', 'O', False), LetterButtons(150, 100, 'p', 'P', False), \
                                                       LetterButtons(200, 100, 'q', 'Q', False), LetterButtons(250, 100, 'r', 'R', False), LetterButtons(300, 100, 's', 'S', False), LetterButtons(350, 100, 't', 'T', False), \
                                                       LetterButtons(400, 100, 'u', 'U', False), LetterButtons(450, 100, 'v', 'V', False), LetterButtons(500, 100, 'w', 'W', False), LetterButtons(550, 100, 'x', 'X', False), \
                                                       LetterButtons(600, 100, 'y', 'Y', False), LetterButtons(650, 100, 'z', 'Z', False)


buttonlist = [Abutton, Bbutton, Cbutton, Dbutton, Ebutton, Fbutton, Gbutton, Hbutton, Ibutton,
              Jbutton, Kbutton, Lbutton, Mbutton, Nbutton, Obutton, Pbutton, Qbutton, Rbutton,
              Sbutton, Tbutton, Ubutton, Vbutton, Wbutton, Xbutton, Ybutton, Zbutton]

categoryFood = regularbuttons(250, 100, 'Food', LIGHT_BLUE, BLACK, 200, 100, 'food')
categorySports = regularbuttons(250, 225, 'Sports', LIGHT_BLUE, BLACK, 200, 100, 'sports')
categoryDrinks = regularbuttons(250, 350, 'Drinks', LIGHT_BLUE, BLACK, 200, 100, 'drinks')

mainmenubtn = regularbuttons(20, 175, 'Menu', LIGHT_BLUE, BLACK, 150, 80, 'menu')
playagainbtn = regularbuttons(20, 275, 'Play again', LIGHT_BLUE, BLACK, 150, 80, 'playagain')

gamebuttons = [mainmenubtn, playagainbtn]
categorybuttonlist = [categoryFood, categorySports, categoryDrinks]

allregulatbuttons = [mainmenubtn, playagainbtn, categoryFood, categorySports, categoryDrinks]

# ---------------------------------------#
# functions                             #
# ---------------------------------------#

# Function to read the puzzle file
def readFile():
    global categories
    global puzzles
    global clues
    fi = open('puzzle.txt', 'r')
    puzzles = [[], [], []]
    clues = [[], [], []]
    categories = []
    for cat in range(3):  # reads categories
        newCat = fi.readline().strip()
        categories.append(newCat)
        n = int(fi.readline().strip())
        for p in range(n):  # reads puzzles
            newPuzzle = fi.readline().strip()
            splitpuzzle = newPuzzle.split(', ')
            puzzles[cat].append(splitpuzzle[0])
            clues[cat].append(splitpuzzle[1])

    fi.close() # Closes the file

# Loads the images and adds them to a list
def loadImg():
    global sadImgList, happyImgList
    sadImgList = []
    happyImgList = []
    for image in range(7):
        fileName = 'hangman' + str(image) + '.png'
        sadImgList.append(pygame.image.load(fileName))
        if image == 0:
            happyImgList.append(pygame.image.load(fileName))
    for image in range(1, 6):
        fileName = 'hangman' + str(image) + '-happy.png'
        happyImgList.append(pygame.image.load(fileName))

# Function that redraws the game window
def redraw_game_window():
    win.fill(GREEN)
    # code to draw things goes here
    if currentscreen == 'menu': # Draws the category buttons when its on the menu screen
        for categorybuttons in categorybuttonlist:
            categorybuttons.draw()

        win.blit(title, (300, 40)) # Draws the title

    if currentscreen == 'game': # Draws objects when its on the game screen
        for buttons in buttonlist:
            buttons.draw()

        # Draws the hangman
        if not goodguess:
            win.blit(sadImgList[mistakes], (200, 150))
        elif goodguess:
            win.blit(happyImgList[mistakes], (200, 150))
        if word != 'out of words':
            win.blit(guesstext, guessrect)
            win.blit(cluetext, cluerect)

        # Prints a message depending on whether the user won or lost
        if status == 'win' or status == 'lose':
            for gamebutton in gamebuttons:
                gamebutton.draw()
            if status == 'win':
                win.blit(wintext, (550, 240))
            elif status == 'lose':
                win.blit(losetext, (550, 240))

        # Draws the main menu button when you have played all the words in this session
        if word == 'out of words':
            win.blit(nowordstext, (160, 440))
            mainmenubtn.draw()

    pygame.display.update()

# Function that selects a random word
def pickword(category):
    global word, clue, finished
    index = categories.index(category)
    word = random.choice(puzzles[index])
    clue = clues[index][puzzles[index].index(word)]
    while word in playedwords and len(playedwords) < 6: # Prevents the played from getting the same word twice while in a session
        word = random.choice(puzzles[index])
        clue = clues[index][puzzles[index].index(word)]
    playedwords.append(word)
    if len(playedwords) > 6: # Stops giving words when all words have been played
        word = 'out of words'
        clue = 'none'
        finished = True

# Creates the list for the guess
def createGuess(word):
    guessword = []
    for letter in word:
        guessword.append('_')
    for position in range(len(guessword)):
        if word[position] == ' ':
            guessword[position] = ' '

    return guessword

# Reset function
def reset(cat):
    global guessword, mistakes, finished, status
    pickword(cat)
    guessword = createGuess(word)
    mistakes = 0
    for buttons in buttonlist:
        buttons.used = False
        buttons.color = LIGHT_BLUE
    finished = False
    status = 'none'

# ---------------------------------------#
# the main program begins here          #
# ---------------------------------------#

readFile()
loadImg()
pygame.display.set_caption('Hangman')

# Main game loop
inPlay = True
while inPlay:
    if currentscreen == 'game':
        pygame.display.set_caption(currentcat + ' - ' + word)

        # Draws the guess word
        realguessword = ' '.join(guessword)
        guesstext = guess_font.render(str(realguessword), True, BLACK)
        guessrect = guesstext.get_rect(center=(700/2, 400))

        # Draws the clue
        cluetext = clue_font.render(str(clue), True, BLACK)
        cluerect = cluetext.get_rect(center=(700/2, 450))

        # Prevents the user from selecting letters when there are no more words available
        if word == 'out of words':
            for letterbuttons in buttonlist:
                letterbuttons.used = True

    redraw_game_window()  # window must be constantly redrawn - animation
    pygame.time.delay(10)  # pause for 10 milliseconds

    # Get the mouses position
    pos = pygame.mouse.get_pos()

    # Plays the sound effects
    if playsound:
        if status == 'win':
            winsound.play()
        elif status == 'lose':
            losesound.play()

        playsound = False

    # Check if the game is over
    if currentscreen == 'game' and checkwin:
        if '_' not in guessword:
            status = 'win'
            finished = True
            playsound = True
        elif mistakes >= 6:
            status = 'lose'
            finished = True
            playsound = True

        checkwin = False

    # Creates the mouse over effect
    for letterbuttons in buttonlist:
        if not finished:
            if letterbuttons.isOver(pos):
                if not letterbuttons.used:
                    letterbuttons.color = highlightcolor
            elif not letterbuttons.isOver(pos) and not letterbuttons.used:
                letterbuttons.color = LIGHT_BLUE

    for letterbuttons in allregulatbuttons:
        if letterbuttons.isOver(pos):
            letterbuttons.color = highlightcolor
        else:
            letterbuttons.color = LIGHT_BLUE

    for event in pygame.event.get():  # check for any events
        # print(event)
        if event.type == pygame.QUIT:  # if user clicks on the window's 'X' button
            inPlay = False  # exit from the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False  # exit from the game
        if event.type == pygame.MOUSEBUTTONDOWN:  # if user clicks anywhere on win
            if currentscreen == 'game':
                for letterbuttons in buttonlist:
                    if letterbuttons.isOver(pos):
                        if not letterbuttons.used:
                            if mistakes < 6:
                                if '_' in guessword:
                                    # Checks if the letter is in the word and does stuff accordingly
                                    if letterbuttons.letter.lower() in word:
                                        letterbuttons.color = GREEN
                                        goodguess = True
                                        for position in range(len(word)):
                                            if word[position] == letterbuttons.letter:
                                                guessword[position] = letterbuttons.letter

                                    else: # If the letter is not in the word
                                        goodguess = False
                                        letterbuttons.color = RED
                                        mistakes += 1
                                    letterbuttons.used = True
                                    usedletters.append(letterbuttons.letter)
                                    checkwin = True


                if finished:
                    # Checks if mouse is over the buttons
                    if mainmenubtn.isOver(pos):
                        currentscreen = 'menu'
                        reset(currentcat)
                        playedwords = []
                        pygame.display.set_caption('Hangman')
                    elif playagainbtn.isOver(pos):
                        reset(currentcat)

                if word == 'out of words':
                    if mainmenubtn.isOver(pos):
                        currentscreen = 'menu'
                        reset(currentcat)
                        playedwords = []
                        pygame.display.set_caption('Hangman')

            # Mouse code for menu
            if currentscreen == 'menu':
                for button in categorybuttonlist:
                    if button.isOver(pos):
                        currentcat = button.category
                        currentscreen = 'game'
                        pickword(currentcat)
                        guessword = createGuess(word)
                        pygame.display.set_caption(word)

# ---------------------------------------#
pygame.quit()  # always quit pygame when done!
