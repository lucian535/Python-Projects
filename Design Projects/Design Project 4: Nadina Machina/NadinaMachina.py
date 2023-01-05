'''
This is the main code for the Nadina-Machina Prototype

this program was created for out patient with multiple sclerosis. This is aimed to help them regain mobility in their arm through the use of assisted exercise to
gamify her experience to keep her motivated.

This is the program which creates the UI as well as collects data from the various sensors and outputs the corresponding processed data to the output devices. 
This will keep track of user data through the use of a textfile.
This is ran on a raspberry pi.

For more information on this design project, it may be found in my notion protfiolio, linked in the readme
'''

import pygame
import os
from threading import Timer
import time
import sys
import random
from datetime import date

from sensor_library import *
from gpiozero import Motor, Buzzer, LED

motor = Motor(12 16)
buzzer = Buzzer(27)

pygame.init()

monitorInfo = pygame.display.Info()
x = monitorInfo.current_w / 2 - 400
y = monitorInfo.current_h / 2 - 350
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

gametitle = 'Nadina - Machina'
filename = 'DP4-Collected_data.txt'

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption(gametitle)


t1 = pygame.font.SysFont('None', 100)
t2 = pygame.font.SysFont('None', 90)
t3 = pygame.font.SysFont('None', 60)
t4 = pygame.font.SysFont('None', 50)
t5 = pygame.font.SysFont('None', 40)
t6 = pygame.font.SysFont('None', 150)
t7 = pygame.font.SysFont('None', 200)
t8 = pygame.font.SysFont('None', 250)


bg_green = (3, 79, 61)
accent_green = (50, 173, 120)
white = (255, 255, 255)
grey = (212, 212, 212)
black = (0, 0, 0)
orange = (230, 116, 9)
green = (3, 179, 0)
red = (227, 2, 2)
yellow = (255, 230, 69)

''' Main Menu'''
title = t1.render(gametitle, True, white)
Train = t2.render('Train', True, black)
Statistics = t2.render('Statistics', True, black)

title_rect = title.get_rect(center=(400, 105))
train_rect = Train.get_rect(center=(205, 330))
statistics_rect = Statistics.get_rect(center=(205, 480))

stattitle = t3.render('Statistics', True, white)


''' Training Screen '''
traintitle = t3.render('Train', True, white)
train2_rect = traintitle.get_rect(center=(400,27))

setval = t3.render('Set Values', True, black)
setval_rect = setval.get_rect(center=(205, 120))

reps = t4.render('Reps:', True, black)
reps_rect = reps.get_rect(center=(110, 210))

timeint = t4.render('Time (s):', True, black)
timeint_rect = timeint.get_rect(center=(110, 290))

applytext = t3.render('Apply', True, black)
applytext_rect = applytext.get_rect(center=(205, 435))

starttext = t3.render('Start', True, black)
starttext_rect = starttext.get_rect(center=(205, 560))

stoptext = t3.render('Stop', True, black)
stoptext_rect = stoptext.get_rect(center=(205, 640))

angletitle = t3.render('Angle', True, black)
angletitle_rect = angletitle.get_rect(center=(595, 120))

angledefaulttext = '--'

tottime = t4.render('Time Elapsed:', True, black)
tottime_rect = tottime.get_rect(center=(485, 520))

reps2 = t4.render('Reps:', True, black)
reps2_rect = reps2.get_rect(center=(552, 450))

uptext = t4.render('UP', True, black)
uptext_rect = uptext.get_rect(center=(520, 360))

downtext = t4.render('DOWN', True, black)
downtext_rect = downtext.get_rect(center=(670, 360))

''' Stats '''
bestscore = t3.render('Best Score:', True, black)
bestscore_rect = bestscore.get_rect(center=(400, 90))

repscompletedtext = t4.render('Reps:', True, black)
repscompletedtext_rect = repscompletedtext.get_rect(center=(170,280))

timesettext = t4.render('Time Set:', True, black)
timesettext_rect = timesettext.get_rect(center=(400, 280))

totaltimeelapsedtext = t4.render('Total Time:', True, black)
totaltimeelapsedtext_rect = totaltimeelapsedtext.get_rect(center=(630, 280))

bestrepstext = t4.render('Most Reps:', True, black)
bestrepstext_rect = bestrepstext.get_rect(center=(250, 470))

longesttime = t4.render('Longest Time:', True, black)
longesttime_rect = longesttime.get_rect(center=(550, 470))

''' Misc '''
backtext = t3.render('<', True, black)

stat2_rect = stattitle.get_rect(center=(400,27))

class buttons:
    def __init__(self, color, x, y, width, height, outline):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline = outline

    def drawbutton(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(screen, self.outline, [self.x, self.y, self.width, self.height], 4)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

TrainButton = buttons(white, 30, 275, 350, 100, black)
StatsButton = buttons(white, 30, 425, 350, 100, black)
backbutton = buttons(white, 5, 5, 40, 40, black)

repinput = buttons(white, 190, 175, 170, 60, black)
timeinput = buttons(white, 190, 255, 170, 60, black)
applybutton = buttons(orange, 100, 400, 210, 70, black)
startbutton = buttons(green, 100, 520, 210, 70, black)
stopbutton = buttons(red, 100, 600, 210, 70, black)

upbox = buttons(black, 445, 320, 150, 70, black)
downbox = buttons(black, 595, 320, 150, 70, black)

MM_button_list = [TrainButton, StatsButton]
TR_button_list = [repinput, timeinput, applybutton, startbutton, stopbutton, upbox, downbox]
TR2_button_list = [applybutton, startbutton,stopbutton]

def collectdata():
    global rand
    rand = random.randint(1,100)
    Timer(0.2, collectdata).start()

def countrepps():
    global currentreps, countreps
    if countreps:
        currentreps += 1
        Timer(2*confirmtime, countrepps).start()

def controlmsg():
    global start, currenttask
    if start:
        if currenttask == 'UP':
            upbox.color = green
            downbox.color = black
            currenttask = 'DOWN'
        elif currenttask == 'DOWN':
            downbox.color = red
            upbox.color = black
            currenttask = 'UP'

        Timer(confirmtime, controlmsg).start()

def changepress():
    global abletopress
    abletopress = True
    startbutton.color = green

def draw():
    global user_text, angletext, start, countreps, confirmrep, counttimess, currenttime, newtime, startcountdown, abletopress, score, refreshdata, PBscore, repscompleted, totaltimeelapsed, settimevalue, dateofcompletion, bestreps, longesttimereached
    if current_screen == 'Main Menu':
        screen.fill(bg_green)
        
        for i in MM_button_list:
            i.drawbutton()
        
        screen.blit(Train, train_rect)
        screen.blit(Statistics, statistics_rect)

        pygame.draw.rect(screen, accent_green, [100, 50, 600, 100])
        pygame.draw.rect(screen, black, [100, 50, 600, 100], 4)

        screen.blit(title, title_rect)
        #pygame.draw.rect(screen, black, [399, 0, 2, 700])

    elif current_screen == 'Training':
        screen.fill(white)

        pygame.draw.rect(screen, black, [0,0,800,50])
        backbutton.drawbutton()

        screen.blit(backtext, (13, 3))

        pygame.draw.rect(screen, black, [30, 80, 350, 300], 5)
        pygame.draw.rect(screen, black, [420, 80, 350, 220], 5)
        screen.blit(setval, setval_rect)
        screen.blit(reps, reps_rect)
        screen.blit(timeint, timeint_rect)


        for i in TR_button_list:
            i.drawbutton()

        reptext_surface = t4.render(reptext, True, black)
        screen.blit(reptext_surface, (200, 190))

        timetext_surface = t4.render(timetext, True, black)
        screen.blit(timetext_surface, (200, 270))

        screen.blit(traintitle, train2_rect)
        screen.blit(applytext, applytext_rect)
        screen.blit(starttext, starttext_rect)
        screen.blit(stoptext, stoptext_rect)
        screen.blit(angletitle, angletitle_rect)
        screen.blit(tottime, tottime_rect)
        screen.blit(reps2, reps2_rect)
        screen.blit(uptext, uptext_rect)
        screen.blit(downtext, downtext_rect)

        if start:
            angletext = t1.render(f'{rand}°', True, black)
            angletext_rect = angletext.get_rect(center=(595, 210))
            screen.blit(angletext, angletext_rect)
            newtime = float(time.time())
            totaltime = t4.render(f'{round(newtime - currenttime, 2)}s', True, black)

            if currentreps >= confirmrep:
                start = False
                countreps = False
                repinput.outline = green
                timeinput.outline = green  
                counttimess = False
                currenttime = round(newtime - currenttime, 2)
                upbox.color = black
                downbox.color = black
                abletopress = False
                startbutton.color = yellow
                Timer(2*confirmtime, changepress).start()
                score = int(currentreps**2 * 2/currenttime * 1000)

                currentdate = date.today()
                
                f = open(filename, 'a')
                f.write(f'{score} {currentreps} {currenttime} {confirmtime} {currentdate}\n')
                f.close()
            
        else:
            angletext = t1.render(f'{angledefaulttext}°', True, black)
            angletext_rect = angletext.get_rect(center=(595, 215))
            screen.blit(angletext, angletext_rect)
            totaltime = t4.render(f'{currenttime} s', True, black)
        
        if startcountdown:
            count = 3
            while count > 0:
                if count == 3:
                    countdowntext = t6.render(f'{count}', True, black)
                elif count == 2:
                    countdowntext = t7.render(f'{count}', True, black)
                elif count == 1:
                    countdowntext = t8.render(f'{count}', True, black)
                    
                screen.fill(white)
                countdowntext_rect = countdowntext.get_rect(center=(400, 350))
                screen.blit(countdowntext, countdowntext_rect)

                pygame.display.update()
    
                count -= 1
                time.sleep(1)
        
        if score:
        
            scoretext = t3.render(f'Score: {score}', True, red)
            scoretext_rect = scoretext.get_rect(center=(595, 630))
            screen.blit(scoretext, scoretext_rect)
        
        totalreps = t4.render(f'{currentreps} / {confirmrep}', True, black)
        screen.blit(totalreps, (635, 435))
        screen.blit(totaltime, (635, 500))

    

    elif current_screen == 'Stats screen':
        screen.fill(white)

        if refreshdata:
            datalist = []
            try:
                f = open(filename, 'r')
            except:
                f = open(filename, 'w')
                f = open(filename, 'r')

            for line in f:
                line = line[:-1]
                itemlist = list(line.split())
                datalist.append(itemlist)
                
            refreshdata = False
        
            if datalist:
                scorelist = []
                repslist = []
                totaltimelist = []
                for i in datalist:
                    scorelist.append(int(i[0]))
                    repslist.append(int(i[1]))
                    totaltimelist.append(float(i[2]))
                PBscore = max(scorelist)
                PBscoredata = datalist[scorelist.index(PBscore)]
                bestreps = str(max(repslist))
                longesttimereached = str(max(totaltimelist))
                PBscore = PBscoredata[0]
                repscompleted = PBscoredata[1]
                totaltimeelapsed = PBscoredata[2]
                settimevalue = PBscoredata[3]
                dateofcompletion = PBscoredata[4]

            else:
                PBscore = '-'
                repscompleted = '-'
                totaltimeelapsed = '-'
                settimevalue = '-'
                dateofcompletion = '-'
                bestreps = '-'
                longesttimereached = '-'


        pygame.draw.rect(screen, black, [0,0,800,50])
        backbutton.drawbutton()

        PBscoretext = t2.render(PBscore, True, green)
        PBscoretext_rect = PBscoretext.get_rect(center=(400, 160))

        DoC = t5.render(f'Achieved on: {dateofcompletion}', True, black)
        DoC_rect = DoC.get_rect(center=(400,210))

        completedreps = t3.render(repscompleted, True, red)
        completedreps_rect = completedreps.get_rect(center=(170, 340))

        settimevaluetext = t3.render(f'{settimevalue}s', True, red)
        settimevaluetext_rect = settimevaluetext.get_rect(center=(400, 340))

        totaltimevaluetext = t3.render(f'{totaltimeelapsed}s', True, red)
        totaltimevaluetext_rect = totaltimevaluetext.get_rect(center=(630, 340))

        longesttimetext = t3.render(f'{longesttimereached}s', True, red)
        longesttimetext_rect = longesttimetext.get_rect(center=(550, 550))

        mostrepstext = t3.render(bestreps, True, red)
        mostrepstext_rect = mostrepstext.get_rect(center=(250, 550))

        screen.blit(PBscoretext, PBscoretext_rect)
        screen.blit(DoC, DoC_rect)
        screen.blit(completedreps, completedreps_rect)
        screen.blit(settimevaluetext, settimevaluetext_rect)
        screen.blit(totaltimevaluetext, totaltimevaluetext_rect)
        screen.blit(mostrepstext, mostrepstext_rect)
        screen.blit(longesttimetext, longesttimetext_rect)
        
        pygame.draw.rect(screen, black, [0, 380, 800, 2])

        screen.blit(backtext, (13, 3))

        screen.blit(stattitle, stat2_rect)
        screen.blit(repscompletedtext, repscompletedtext_rect)
        screen.blit(bestscore, bestscore_rect)
        screen.blit(timesettext, timesettext_rect)
        screen.blit(totaltimeelapsedtext, totaltimeelapsedtext_rect)
        screen.blit(longesttime, longesttime_rect)
        screen.blit(bestrepstext, bestrepstext_rect)


    pygame.display.update()


collectdata()

current_screen = 'Main Menu'

reptext = ''
repuse = False
timetext = ''
timeuse = False

confirmrep = '-'
currentreps = '-'
currenttime = '-'
confirmtime = ''

run = True
applied = False
start = False

confirmstart = False

countreps = False
counttimess = False
startcountdown = False
abletopress = True
refreshdata = False

score = ''
PBscore = '-'
repscompleted = '-'
totaltimeelapsed = '-'
settimevalue = '-'
dateofcompletion = '-'
bestreps = '-'
longesttimereached = '-'

while run:

    draw()

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        if current_screen == 'Main Menu':
            for i in MM_button_list:
                if i.isOver(pos):
                    i.color = grey              
                    if event.type == pygame.MOUSEBUTTONUP:
                        if i == TrainButton:
                            current_screen = 'Training'
                        elif i == StatsButton:
                            current_screen = 'Stats screen'
                            refreshdata = True
                else:
                    i.color = white

        elif current_screen == 'Training':

            if repuse:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        reptext = reptext[:-1]
                    else:
                        if len(reptext) < 8:
                            reptext += event.unicode
            if timeuse:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        timetext = timetext[:-1]
                    else:
                        if len(timetext) < 8:
                            timetext += event.unicode

            if backbutton.isOver(pos):
                if event.type == pygame.MOUSEBUTTONUP:
                    current_screen = 'Main Menu'
            
            if not start:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if repinput.isOver(pos):
                        repinput.color = grey
                        repinput.outline = black
                        timeinput.outline = black
                        repuse = True
                    elif not repinput.isOver(pos):
                        repinput.color = white
                        repuse = False
                    if timeinput.isOver(pos):
                        timeinput.color = grey
                        repinput.outline = black
                        timeinput.outline = black
                        timeuse = True
                    elif not timeinput.isOver(pos):
                        timeinput.color = white
                        timeuse = False

            for i in TR2_button_list:
                if i.isOver(pos):
                    if event.type == pygame.MOUSEBUTTONUP:
                        if i == applybutton:
                            try:
                                confirmrep = int(reptext)
                                confirmtime = float(timetext)
                                print(confirmrep, confirmtime)
                                repinput.outline = green
                                timeinput.outline = green
                                applied = True
                            except:
                                pass
                        if i == startbutton:
                            if applied:
                                if not start:
                                    if confirmrep == int(reptext) and confirmtime == float(timetext):
                                        if abletopress:
                                            startcountdown = True
                                            draw()
                                            startcountdown = False
                                            start = True
                                            repinput.outline = red
                                            timeinput.outline = red  
                                            countreps = True
                                            currenttime = time.time()
                                            currentreps = 0
                                            counttimess = True
                                            currenttask = 'UP'
                                            controlmsg()
                                            Timer(2*confirmtime, countrepps).start()
                        if i == stopbutton:
                            if start:
                                start = False
                                abletopress = False
                                startbutton.color = yellow
                                Timer(2*confirmtime, changepress).start()
                                countreps = False
                                repinput.outline = green
                                timeinput.outline = green  
                                currenttime = round(newtime - currenttime, 2)
                                upbox.color = black
                                downbox.color = black

        elif current_screen == 'Stats screen':
            if backbutton.isOver(pos):
                if event.type == pygame.MOUSEBUTTONUP:
                    current_screen = 'Main Menu'

pygame.quit()
