from sounds import *
import pygame, sys
from pygame.locals import *

WIDTH = 1400
HEIGHT = 800
LEFT_BOX = 200
BOTTOM_BOX = 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GOLD = (255, 223, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
beats = 6
instruments = 6
box_w = (WIDTH-LEFT_BOX) // beats
box_h = (HEIGHT-BOTTOM_BOX) // instruments
fps = 60
borders1 = 5
borders2 = 3
clock = pygame.time.Clock()
active_boxes = [[False for _ in range(beats)] for _ in range(instruments)]
playing = True
active_beat = 0
active_length = 0
beat_changed = False
beat_length = fps // beats
mixer.set_num_channels(3*instruments)

def draw_grid():
    left_box = pygame.draw.rect(screen, GRAY,
        [0, 0, LEFT_BOX, HEIGHT - BOTTOM_BOX], 5)
    bottom_menu = pygame.draw.rect(screen, GRAY,
        [0, HEIGHT - BOTTOM_BOX, WIDTH, BOTTOM_BOX])
    boxes = []
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
        pygame.draw.line(screen, GRAY, (0, (i + 1) * box_h),
        (LEFT_BOX, (i + 1) * box_h), borders2)

    for i in range(beats):
        for j in range(instruments):
            box = pygame.draw.rect(
                screen,
                GOLD,
                (
                    LEFT_BOX + (i * box_w),
                    j * box_h,
                    box_w,
                    box_h
                ),
                borders2,
                5
            )
            box = pygame.draw.rect(
                screen,
                GREEN if active_boxes[j][i] else GRAY,
                (
                    LEFT_BOX + (i * box_w) + borders1,
                    j * box_h + borders1,
                    box_w - (2 * borders1),
                    box_h - (2 * borders1)
                ),
                0,
                5
            )
            boxes.append((box, (i, j)))

    active_box = pygame.draw.rect(
        screen,
        BLUE,
        (
            LEFT_BOX + (active_beat * box_w),
            0,
            box_w,
            HEIGHT-BOTTOM_BOX
        ),
        borders1,
        3
    )
    return boxes

def play_notes():
    for i in range(len(active_boxes)):
        if active_boxes[i][active_beat]:
            inst_sounds[i].play()

if __name__ == '__main__':
    while True:
        clock.tick(fps)
        screen.fill(BLACK)
        boxes = draw_grid()
        if beat_changed:
            play_notes()
            beat_changed = False
        if playing:
            if active_length < beat_length:
                active_length += 1
            else:
                active_length = 0
                beat_changed = True
                active_beat = (active_beat + 1) % beats
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if event.pos[0] > LEFT_BOX and event.pos[1] < HEIGHT-BOTTOM_BOX:
                        col = (event.pos[0] - LEFT_BOX) // box_w
                        row = event.pos[1] // box_h
                        active_boxes[row][col] = not active_boxes[row][col]
        pygame.display.update()