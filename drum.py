import os.path
from sounds import *
import pygame, sys
from pygame.locals import *
import requests

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
fps = 60
borders1 = 5
borders2 = 3
clock = pygame.time.Clock()

class Beat:
    
    def __init__(self, beats = 16, bpm = 5, instruments = 6,
                    font_name = 'Roboto-Bold.ttf', font_size = 32,
                    active_boxes = None):
        self.beats = beats
        self.bpm = bpm
        self.instruments = instruments
        if active_boxes is not None:
            self.active_boxes = active_boxes
        else:
            self.active_boxes = [[False for _ in range(beats)] for _ in range(instruments)]
        self.beat_length = fps // bpm
        self.playing = True
        self.active_beat = 0
        self.active_length = 0
        self.beat_changed = False
        validate_font(font_name)
        self.label_font = pygame.font.Font(font_name, font_size)
        self.box_w = (WIDTH-LEFT_BOX) // beats
        self.box_h = (HEIGHT-BOTTOM_BOX) // instruments
        mixer.set_num_channels(3*self.instruments)

    def update(self):
        self.draw_grid()
        self.draw_settings()
        if self.beat_changed:
            self.play_notes()
            self.beat_changed = False
        if self.playing:
            if self.active_length < self.beat_length:
                self.active_length += 1
            else:
                self.active_length = 0
                self.beat_changed = True
                self.active_beat = (self.active_beat + 1) % self.beats
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if event.pos[0] > LEFT_BOX and \
                        event.pos[1] < HEIGHT-BOTTOM_BOX:
                        col = (event.pos[0] - LEFT_BOX) // self.box_w
                        row = event.pos[1] // self.box_h
                        self.active_boxes[row][col] = not self.active_boxes[row][col]

    def draw_grid(self):
        left_box = pygame.draw.rect(screen, GRAY, [0, 0, LEFT_BOX, HEIGHT - BOTTOM_BOX], 5)
        bottom_box = pygame.draw.rect(screen, GRAY, [0, HEIGHT - BOTTOM_BOX, WIDTH, BOTTOM_BOX])
        boxes = []
        hi_hat_text = self.label_font.render('Hi Hat', True, WHITE)
        screen.blit(hi_hat_text,(30, 30))
        snare_text = self.label_font.render('Snare', True, WHITE)
        screen.blit(snare_text,(30, 130))
        kick_text = self.label_font.render('Bass Drum', True, WHITE)
        screen.blit(kick_text,(30, 230))
        crash_text = self.label_font.render('Crash', True, WHITE)
        screen.blit(crash_text,(30, 330))
        clap_text = self.label_font.render('Clap', True, WHITE)
        screen.blit(clap_text,(30, 430))
        floor_text = self.label_font.render('Floor Tom', True, WHITE)
        screen.blit(floor_text,(30, 530))
        
        self.box_w = (WIDTH-LEFT_BOX) // self.beats
        self.box_h = (HEIGHT-BOTTOM_BOX) // self.instruments

        for i in range(self.instruments):
            pygame.draw.line(screen, GRAY, (0, (i + 1) * self.box_h),
            (LEFT_BOX, (i + 1) * self.box_h), borders2)

        for i in range(self.beats):
            for j in range(self.instruments):
                box = pygame.draw.rect(
                    screen,
                    GOLD,
                    (
                        LEFT_BOX + (i * self.box_w),
                        j * self.box_h,
                        self.box_w,
                        self.box_h
                    ),
                    borders2,
                    5
                )
                box = pygame.draw.rect(
                    screen,
                    GREEN if self.active_boxes[j][i] else GRAY,
                    (
                        LEFT_BOX + (i * self.box_w) + borders1,
                        j * self.box_h + borders1,
                        self.box_w - (2 * borders1),
                        self.box_h - (2 * borders1)
                    ),
                    0,
                    5
                )
                boxes.append((box, (i, j)))

        active_box = pygame.draw.rect(
            screen,
            BLUE,
            (
                LEFT_BOX + (self.active_beat * self.box_w),
                0,
                self.box_w,
                HEIGHT-BOTTOM_BOX
            ),
            borders1,
            3
        )
        return boxes

    def draw_settings(self):
        bpm_text = self.label_font.render('BPM', True, WHITE)
        screen.blit(bpm_text, (100, HEIGHT - BOTTOM_BOX + 40))
        bpm_up_text = self.label_font.render('+', True, WHITE)
        screen.blit(bpm_up_text, (243, HEIGHT - BOTTOM_BOX + 82))
        bpm_down_text = self.label_font.render('-', True, WHITE)
        screen.blit(bpm_down_text, (120, HEIGHT - BOTTOM_BOX + 82))
        bpm_counter_text = self.label_font.render(str(self.bpm), True, WHITE)
        screen.blit(bpm_counter_text, (180, HEIGHT - BOTTOM_BOX + 82))
        pygame.draw.rect(screen, BLACK, [98, HEIGHT - BOTTOM_BOX + 73, 179, 54], 2,5)
        pygame.draw.rect(screen, GREEN, [100, HEIGHT - BOTTOM_BOX + 75, 50, 50], 1, border_top_left_radius=5, border_bottom_left_radius=5)
        pygame.draw.rect(screen, GREEN, [150, HEIGHT - BOTTOM_BOX + 75, 75, 50], 1)
        pygame.draw.rect(screen, GREEN, [225, HEIGHT - BOTTOM_BOX + 75, 50, 50], 1, border_bottom_right_radius=5, border_top_right_radius=5)

    def play_notes(self):
        for i in range(len(self.active_boxes)):
            if self.active_boxes[i][self.active_beat]:
                inst_sounds[i].play()


def validate_font(font_name):
    '''
        Validates if the font file exists
        There should be a .ttf file in the root directory, downloads Roboto Bold
        from the site Download Free Fonts if there's not
    '''
    if os.path.exists(font_name):
        return
    try:
        req = requests.get("https://www.img.download-free-fonts.com/dl.php?id=31207")
        with open(font_name, "wb+") as font_file:
            font_file.write(req.content)
        return
    except:
        print("Exception retrieving the font")
        exit()


if __name__ == '__main__':
    beat = Beat()

    while True:
        clock.tick(fps)
        screen.fill(BLACK)
        beat.update()
        pygame.display.update()