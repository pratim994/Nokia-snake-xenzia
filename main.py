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




def isGameOver():
    






def food_spawn():


def score():


if __init__ == "__main__":
