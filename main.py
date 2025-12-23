import pygame
import sys
import random
import tkinter as tk
from tkinter import Tk, Label, Button

pygame.init()

# Constants
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = DISPLAY_WIDTH // GRID_SIZE
GRID_HEIGHT = DISPLAY_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (140, 8, 8)
GREEN = (8, 140, 10)
YELLOW = (209, 209, 8)
BRIGHT_GREEN = (137, 244, 66)
BRIGHT_YELLOW = (239, 239, 98)
BRIGHT_RED = (226, 71, 61)
GRAY = (50, 50, 50)
DARK_GRAY = (7, 7, 7)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SNAKE XENZIA")
fps = pygame.time.Clock()

# Sounds (make sure these files exist in the same folder)
pygame.mixer.music.load("background.wav")
loser_sound = pygame.mixer.Sound("loser.wav")
score_sound = pygame.mixer.Sound("score.wav")

# Fonts
def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(display, ac, (x, y, w, h))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(display, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 30)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = (x + w // 2, y + h // 2)
    display.blit(text_surf, text_rect)

def message_display(text, size=50, color=BLACK, y_offset=0):
    font = pygame.font.Font(None, size)
    text_surf, text_rect = text_objects(text, font, color)
    text_rect.center = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + y_offset)
    display.blit(text_surf, text_rect)

def instructions():
    root = Tk()
    root.title("Instructions")
    root.geometry("500x400")
    msg = (
        "CONTROLS\n"
        "Use ARROW KEYS to move the snake.\n\n"
        "LEVEL: NOOB\n"
        "• Snake can pass through walls (wrap around)\n"
        "• Game ends only if snake eats itself\n\n"
        "LEVEL: PRO\n"
        "• Snake dies on hitting walls\n"
        "• Game ends on wall hit or eating itself"
    )
    Label(root, text=msg, font=("Verdana", 12), justify="left").pack(pady=20, padx=20)
    Button(root, text="OK", command=root.destroy, width=10).pack()
    root.mainloop()

def game_over(score):
    pygame.mixer.music.stop()
    loser_sound.play()
    root = Tk()
    root.title("GAME OVER")
    Label(root, text=f"Your Score: {score}", font=("Verdana", 20)).pack(pady=50)
    Button(root, text="QUIT", command=sys.exit, width=10).pack()
    root.mainloop()

# Base Snake Class (shared logic)
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.position = [100, 100]
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self, direction):
        if (direction == "RIGHT" and self.direction != "LEFT") or \
           (direction == "LEFT" and self.direction != "RIGHT") or \
           (direction == "UP" and self.direction != "DOWN") or \
           (direction == "DOWN" and self.direction != "UP"):
            self.change_to = direction

    def move(self, food_pos):
        # Update head
        if self.change_to == "RIGHT": self.position[0] += GRID_SIZE
        if self.change_to == "LEFT":  self.position[0] -= GRID_SIZE
        if self.change_to == "UP":    self.position[1] -= GRID_SIZE
        if self.change_to == "DOWN":  self.position[1] += GRID_SIZE

        self.direction = self.change_to
        self.body.insert(0, list(self.position))

        # Check if food eaten
        if abs(self.position[0] - food_pos[0]) < 10 and abs(self.position[1] - food_pos[1]) < 10:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self):
        # Self collision
        if self.position in self.body[1:]:
            return True
        return False

    def get_head(self):
        return self.position

    def get_body(self):
        return self.body

# PRO Mode Snake (walls kill)
class ProSnake(Snake):
    def check_collision(self):
        if super().check_collision():
            return True
        # Wall collision
        if (self.position[0] < 20 or self.position[0] >= DISPLAY_WIDTH - 20 or
            self.position[1] < 20 or self.position[1] >= DISPLAY_HEIGHT - 20):
            return True
        return False

# NOOB Mode Snake (wrap around)
class NoobSnake(Snake):
    def move(self, food_pos):
        eaten = super().move(food_pos)
        # Wrap around
        if self.position[0] < 0: self.position[0] = DISPLAY_WIDTH - GRID_SIZE
        if self.position[0] >= DISPLAY_WIDTH: self.position[0] = 0
        if self.position[1] < 0: self.position[1] = DISPLAY_HEIGHT - GRID_SIZE
        if self.position[1] >= DISPLAY_HEIGHT: self.position[1] = 0
        self.body[0] = list(self.position)
        return eaten

    def check_collision(self):
        return super().check_collision()  # Only self-eat ends game

class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.position = [
            random.randint(1, GRID_WIDTH - 2) * GRID_SIZE,
            random.randint(1, GRID_HEIGHT - 2) * GRID_SIZE
        ]
        self.on_screen = True

    def hide(self):
        self.on_screen = False

def draw_grid():
    for x in range(0, DISPLAY_WIDTH, GRID_SIZE):
        pygame.draw.line(display, DARK_GRAY, (x, 0), (x, DISPLAY_HEIGHT))
    for y in range(0, DISPLAY_HEIGHT, GRID_SIZE):
        pygame.draw.line(display, DARK_GRAY, (0, y), (DISPLAY_WIDTH, y))

def draw_walls():
    thickness = 20
    pygame.draw.rect(display, GRAY, (0, 0, DISPLAY_WIDTH, thickness))  # top
    pygame.draw.rect(display, GRAY, (0, DISPLAY_HEIGHT - thickness, DISPLAY_WIDTH, thickness))  # bottom
    pygame.draw.rect(display, GRAY, (0, 0, thickness, DISPLAY_HEIGHT))  # left
    pygame.draw.rect(display, GRAY, (DISPLAY_WIDTH - thickness, 0, thickness, DISPLAY_HEIGHT))  # right

def game_loop(mode="pro"):
    global score
    score = 0
    pygame.mixer.music.play(-1)

    if mode == "pro":
        snake = ProSnake()
    else:
        snake = NoobSnake()

    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")

        # Move snake
        if snake.move(food.position):
            score += 1
            score_sound.play()
            food.hide()

        if not food.on_screen:
            food.spawn()

        # Check collision
        if snake.check_collision():
            game_over(score)

        # Draw everything
        display.fill(BLACK)
        draw_grid()
        if mode == "pro":
            draw_walls()

        # Draw snake
        for segment in snake.get_body():
            pygame.draw.circle(display, SNAKE_COLOR, (segment[0] + 10, segment[1] + 10), 10)

        # Draw food
        pygame.draw.rect(display, FOOD_COLOR, (*food.position, GRID_SIZE, GRID_SIZE))

        # Update caption
        pygame.display.set_caption(f"SNAKE XENZIA ||| SCORE: {score}")
        pygame.display.flip()
        fps.tick(10)

def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display.fill(WHITE)
        message_display("SNAKE XENZIA", 60, BLACK, -100)

        button("Noob", 100, 200, 150, 70, GREEN, BRIGHT_GREEN, lambda: game_loop("noob"))
        button("Pro", 350, 200, 150, 70, GREEN, BRIGHT_GREEN, lambda: game_loop("pro"))
        button("Instructions", 200, 300, 200, 70, YELLOW, BRIGHT_YELLOW, instructions)
        button("Quit", 200, 400, 200, 70, RED, BRIGHT_RED, sys.exit)

        pygame.display.update()
        fps.tick(15)

# Start the game
game_intro()