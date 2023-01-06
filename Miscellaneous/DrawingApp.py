import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Paint')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 149, 0)
pink = (255, 0, 255)

screen.fill(white)

font1 = pygame.font.SysFont('comicsans', 70)

restarttext = font1.render('X', True, (227, 34, 34))
erasertext = font1.render('E', True, (255, 87, 229))

size1text = font1.render('S', True, black)
size2text = font1.render('M', True, black)
size3text = font1.render('L', True, black)


class sketch:
    def __init__(self, radius, color, x, y):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y

    def drawShape(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class button:
    def __init__(self, x, y, width, height, color, outlinecolor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outlinecolor = outlinecolor

    def drawButton(self, text):
        self.text = text
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(screen, self.outlinecolor, [self.x, self.y, self.width, self.height], 5)
        screen.blit(self.text, (self.x + 5, self.y + 5))

    def drawColorButton(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(screen, self.outlinecolor, [self.x, self.y, self.width, self.height], 5)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class outline:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def drawOutline(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 5)


pencil = sketch(5, black, 0, 0)

restartbutton = button(940, 740, 50, 50, (168, 20, 20), (227, 34, 34))
eraser = button(880, 740, 50, 50, (247, 148, 232), black)

largebutton = button(820, 740, 50, 50, white, black)
medbutton = button(760, 740, 50, 50, white, black)
smallbutton = button(700, 740, 50, 50, white, black)

blackbutton = button(10, 740, 50, 50, black, black)
redbutton = button(70, 740, 50, 50, red, black)
bluebutton = button(130, 740, 50, 50, blue, black)
greenbutton = button(190, 740, 50, 50, green, black)
yellowbutton = button(250, 740, 50, 50, yellow, black)
orangebutton = button(310, 740, 50, 50, orange, black)
pinkbutton = button(370, 740, 50, 50, pink, black)

goldoutline_colors = outline(10, 740, 50, 50, (255, 211, 69))
goldoutline_size = outline(700, 740, 50, 50, (255, 211, 69))

buttonname = [blackbutton, redbutton, bluebutton, greenbutton, yellowbutton, orangebutton, pinkbutton]
buttoncolor = [black, red, blue, green, yellow, orange, pink]

def draw():
    pygame.draw.rect(screen, (171, 171, 171), [0, 730, 1000, 80])
    pygame.draw.rect(screen, black, [0, 730, 1000, 80], 5)

    restartbutton.drawButton(restarttext)
    eraser.drawButton(erasertext)

    largebutton.drawButton(size3text)
    medbutton.drawButton(size2text)
    smallbutton.drawButton(size1text)

    for i in buttonname:
        i.drawColorButton()

    goldoutline_colors.drawOutline()
    goldoutline_size.drawOutline()

    pygame.display.update()


run = True
while run:
    draw()

    sizebuttons = [smallbutton, medbutton, largebutton]

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            if 0 <= pos[1] <= 720:
                for buttonnames in sizebuttons:
                    if goldoutline_size.x == buttonnames.x and goldoutline_size.y == buttonnames.y:
                        pencil.x = pos[0]
                        pencil.y = pos[1]
                        pencil.drawShape()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartbutton.isOver(pos):
                screen.fill(white)
            if eraser.isOver(pos):
                pencil.color = white
                goldoutline_colors.x = eraser.x
                goldoutline_colors.y = eraser.y

            if largebutton.isOver(pos):
                pencil.radius = 30
                goldoutline_size.x = largebutton.x
                goldoutline_size.y = largebutton.y
            if medbutton.isOver(pos):
                pencil.radius = 15
                goldoutline_size.x = medbutton.x
                goldoutline_size.y = medbutton.y
            if smallbutton.isOver(pos):
                pencil.radius = 5
                goldoutline_size.x = smallbutton.x
                goldoutline_size.y = smallbutton.y

            for button, colour in zip(buttonname, buttoncolor):
                if button.isOver(pos):
                    pencil.color = colour
                    goldoutline_colors.x = button.x
                    goldoutline_colors.y = button.y

