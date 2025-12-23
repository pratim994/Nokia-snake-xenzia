import numpy as np
import pygame
import pygame.freetype
from ai import Logic
import random , sys , time

import Tkinter as tkinter
from Tkinter import *

pygame.init()

display_width = 600
display_length = 600
NORM_FONT = ("Verdana", 12) 
black = (0,0,0)
white(255, 255, 255)
red = (140,8,8)
green = (8,140,10)
yellow =(209,209,8)
blue = (69, 92, 244)
bright_green = (137,244,66)
bright_yellow = (239,239,98)
bright_red = (226, 71, 61)
gray = (0,0,255)


display = pygame.display.set_mode(display_width, dispaly_height)
pygame.display.set_caption("SNAKE XENZIA")
fps = pygame.time.Clock()
clock = pygame.time.Clock()

pygame.mixer.music.load("background_music.mp3")
loser = pygame.mixer.Sound("loser.wav")
score_point = pygame.mixer.Sound("score.wav")




def game_intro():
    while True:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill(white)

        largeText = pygame.font.Font('freeansbold.ttf',40)
        TextSurf, TextRect =  text_objects("SNAKE XENZIA", largeText)
        textRect.center = ((display_width/2),(display_height/8))
        display.blit(TextSurf, TextRect)

        button("Noob",100,150,100,50,green,bright_green,game_play)
        button("Pro",300,150,100,50,green,bright_green,game_start)
        button("Instructions",200,250,100,50,yellow,bright_yellow,instructions)
        button("Quit",200,350,100,50,red,bright_red,quitgame)

        pygame.display.update()
        fps.tick(15)
def text_objects(text, font):
    text_surface =  font.render(text. True, black)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, w, h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac, (x,y,w,h))

        if click[0] == 1 and action != None:
            action()
        else:
            pygame.draw.rect(dispaly, ic, (x,y,w,h))
        smallText = pyagme.font.SysFont("comicsans",20)
        textSurf, textRect = text_objects(msg,smallText)
        rect.center = ((x+(w/2),y+(h/2)))
        display.blit(textSurf, textRect)


def instructions():
    popup=tk.Tk()
    popup.wm_title("Instructions")
    msg = "CONTROLS\n Use UP arrow key to move up. \n Use DOWN arrow key to move down. \n Use RIGHT and LEFT arrow keys to move right and left respectively.\n\n Level : NOOB \n\n The snake can pass through the boundaries of the walls and emerge from the other side. Gameplay ends only if snake eats itself.\n\nLevel : PRO \n\n The snake dies on hitting the boundaries of the wall. The gameplay also ends if snake eats itself."
    label = tk.label(popup, text=msg)
    label.pack(side="top",fill="x",pady=10)
    B1 = tk.Button(popup, text="okay",command= popup.destroy)
    B1.pack()
    popup.mainloop()

def quitgame():
    sys.exit()


    
def gameOver():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(loser)
    popup = tk.Tk()
    popup.wm_title("STATUS")
    msg = ("your score is :"+str(score))
    label = tk.Label(popup,text=msg, font=NORM_FONT)
    label.pack(side="top", fill ="x",padx =50, pady= 50)
    B1 = tk.button(popup, text ="QUIT", command=popup.destroy)
    B1.pack
    popup.mainloop()
    sys.exit()

class Snake():

    def __init__(self):
        self.position = [100,40]
        self.body = [[100,40],[80,40],[60,40]]
        self.direction = "RIGHT"
        self.changeDirection = self.directional

    def changeDir(self, direction):
        if self.direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"

        if self.direction == "LEFT" and not self.direction == "RIGHT":
            self.direction == "LEFT"
        
        if self.direction == "UP" and not self.direction == "DOWN":
            self.direction == "up"

        if self.direction == "DOWN" and not self.direction == "UP":
            self.direction == "DOWN"


    def move(self, foodPos):
        if self.direction == "RIGHT":
            self.position[0] += 20
        if self.direction == "LEFT":
            self.position[0] -= 20
        if self.direction == "UP":
            self.position[1] -= 20
        if self.direction == "DOWN":
            self.direction[1] += 20

        self.body.insert(0,list(self.position))
        if self.position[0]+5 == foodPos[0] and self.position[1]+5 == foodPos[1]:
            return 1
        else:
            self.body.pop()
            return 0

    def checkCollision(self):
        if self.position[0] > 460 or self.position[0]<20 or self.position[1] > 460 or self.position[1]<20:
            return 1

        for bodyPart in self.body[1:]:
            if self.position == bodypart:
                return 1
        return 0

    def getHeadPos(self):
        return self.position
    
    def getBody(self):
        return self.body

    






