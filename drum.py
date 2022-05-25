from tkinter import LEFT
import pygame, sys
from pygame import mixer
from pygame.locals import *

WIDTH = 1400
HEIGHT = 800
LEFT_BOX = 200
BOTTOM_BOX = 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
beats = 8
instruments = 6
box_w = (WIDTH-LEFT_BOX) // beats
box_h = (HEIGHT-BOTTOM_BOX) // instruments
fps = 60
clock = pygame.time.Clock()
active = [[True for _ in range(beats)] for _ in range(instruments)]


def draw_grid():
    left_box = pygame.draw.rect(screen, GRAY, [0, 0, LEFT_BOX, HEIGHT - BOTTOM_BOX], 5)
    bottom_menu = pygame.draw.rect(screen, GRAY,[0, HEIGHT - BOTTOM_BOX, WIDTH, BOTTOM_BOX])
    boxes = []
    colors = [GRAY, WHITE, GRAY]
    hi_hat_text = label_font.render('Hi Hat', True, WHITE)
    screen.blit(hi_hat_text,(30, 30))
    snare_text = label_font.render('Snare', True, WHITE)
    screen.blit(snare_text,(30, 130))
    kick_text = label_font.render('Bass Drum', True, WHITE)
    screen.blit(kick_text,(30, 230))
    crash_text = label_font.render('Crash', True, WHITE)
    screen.blit(crash_text,(30, 330))
    clap_text = label_font.render('Clap', True, WHITE)
    screen.blit(clap_text,(30, 430))
    floor_text = label_font.render('Floor Tom', True, WHITE)
    screen.blit(floor_text,(30, 530))
    
    box_w = (WIDTH-LEFT_BOX) // beats
    box_h = (HEIGHT-BOTTOM_BOX) // instruments

    for i in range(instruments):
        pygame.draw.line(screen, GRAY, (0, (i + 1) * 100), (LEFT_BOX, (i + 1) * 100), 3)

    for i in range(beats):
        for j in range(instruments):
            box = pygame.draw.rect(screen, GRAY if active[j][i] else WHITE, (LEFT_BOX + (i * box_w), j * box_h, box_w, box_h), 2)
            boxes.append((box, (i, j)))
    return boxes


while True:
    clock.tick(fps)
    screen.fill(BLACK)
    boxes = draw_grid()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if event.pos[0] > LEFT_BOX and event.pos[1] < HEIGHT-BOTTOM_BOX:
                    col = (event.pos[0] - LEFT_BOX) // box_w
                    row = event.pos[1] // box_h
                    active[row][col] = not active[row][col]
    pygame.display.update()