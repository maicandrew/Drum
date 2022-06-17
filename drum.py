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
font_name = 'Roboto-Bold.ttf'
label_font = None

class Beat:
    
    def __init__(self, beats = 16, bpm = 5, instruments = 6, active_boxes = None):
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
        self.box_w = (WIDTH-LEFT_BOX) // beats
        self.box_h = (HEIGHT-BOTTOM_BOX) // instruments
        mixer.set_num_channels(3*self.instruments)

    def update(self):
        '''
            Updates the state of the beat every frame
        '''
        self.draw_grid()
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

    def draw_grid(self):
        '''
            Draws the grid with the current beat with the respective color
            Green for the active boxes and Black for the inactive ones
        '''
        left_box = pygame.draw.rect(screen, GRAY, [0, 0, LEFT_BOX, HEIGHT - BOTTOM_BOX], 5)
        bottom_box = pygame.draw.rect(screen, GRAY, [0, HEIGHT - BOTTOM_BOX, WIDTH, BOTTOM_BOX])
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

    def play_notes(self):
        '''
            Plays the notes for the current active boxes on the beat
        '''
        for i in range(len(self.active_boxes)):
            if self.active_boxes[i][self.active_beat]:
                inst_sounds[i].play()

class Settings:

    def __init__(self, beat):
        self.beat = beat
        self.bpm_down = pygame.draw.rect(
            screen, 
            GREEN,
            [100, HEIGHT - BOTTOM_BOX + 75, 50, 50],
            1,
            border_top_left_radius=5,
            border_bottom_left_radius=5
        )
        self.bpm_up = pygame.draw.rect(
            screen,
            GREEN,
            [225, HEIGHT - BOTTOM_BOX + 75, 50, 50],
            1,
            border_bottom_right_radius=5,
            border_top_right_radius=5
        )
        self.beats_down = None
        self.beats_up = None
        self.label_font = label_font

    def draw(self):
        '''
            Draws the current settings and the options to increment or decrement
                * BPM
                *Beats on screen
        '''

        #BPM
        bpm_text = label_font.render('BPM', True, WHITE)
        screen.blit(bpm_text, (100, HEIGHT - BOTTOM_BOX + 40))
        bpm_up_text = label_font.render('+', True, WHITE)
        screen.blit(bpm_up_text, (243, HEIGHT - BOTTOM_BOX + 82))
        bpm_down_text = label_font.render('-', True, WHITE)
        screen.blit(bpm_down_text, (120, HEIGHT - BOTTOM_BOX + 82))
        bpm_counter_text = label_font.render(str(self.beat.bpm), True, WHITE)
        screen.blit(bpm_counter_text, (180, HEIGHT - BOTTOM_BOX + 82))
        pygame.draw.rect(screen, BLACK,
            [98, HEIGHT - BOTTOM_BOX + 73, 179, 54], 2,5)
        pygame.draw.rect(screen, GREEN,
            [150, HEIGHT - BOTTOM_BOX + 75, 75, 50], 1)
        self.bpm_down = pygame.draw.rect(
            screen,
            GREEN,
            [100, HEIGHT - BOTTOM_BOX + 75, 50, 50],
            1,
            border_top_left_radius=5,
            border_bottom_left_radius=5
        )
        self.bpm_up = pygame.draw.rect(
            screen,
            GREEN,
            [225, HEIGHT - BOTTOM_BOX + 75, 50, 50],
            1,
            border_bottom_right_radius=5,
            border_top_right_radius=5
        )

        #Beats on Screen
        beats_text = label_font.render('Beats', True, WHITE)
        screen.blit(beats_text, (400, HEIGHT - BOTTOM_BOX + 40))
        beats_up_text = label_font.render('+', True, WHITE)
        screen.blit(beats_up_text, (543, HEIGHT - BOTTOM_BOX + 82))
        beats_down_text = label_font.render('-', True, WHITE)
        screen.blit(beats_down_text, (420, HEIGHT - BOTTOM_BOX + 82))
        beats_counter_text = label_font.render(str(self.beat.beats), True, WHITE)
        screen.blit(beats_counter_text, (480, HEIGHT - BOTTOM_BOX + 82))
        pygame.draw.rect(screen, BLACK,
            [398, HEIGHT - BOTTOM_BOX + 73, 179, 54], 2,5)
        pygame.draw.rect(screen, GREEN,
            [450, HEIGHT - BOTTOM_BOX + 75, 75, 50], 1)
        self.beats_down = pygame.draw.rect(
            screen,
            GREEN,
            [400, HEIGHT - BOTTOM_BOX + 75, 50, 50],
            1,
            border_top_left_radius=5,
            border_bottom_left_radius=5
        )
        self.beats_up = pygame.draw.rect(
            screen,
            GREEN,
            [525, HEIGHT - BOTTOM_BOX + 75, 50, 50],
            1,
            border_bottom_right_radius=5,
            border_top_right_radius=5
        )

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
    validate_font(font_name)
    label_font = pygame.font.Font(font_name, 32)
    beat = Beat()
    settings = Settings(beat)

    while True:
        clock.tick(fps)
        screen.fill(BLACK)
        beat.update()
        settings.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if event.pos[0] > LEFT_BOX and \
                        event.pos[1] < HEIGHT-BOTTOM_BOX:
                        col = (event.pos[0] - LEFT_BOX) // beat.box_w
                        row = event.pos[1] // beat.box_h
                        beat.active_boxes[row][col] = not beat.active_boxes[row][col]
                    elif settings.bpm_down.collidepoint(event.pos):
                        beat.bpm = max(1, beat.bpm - 1)
                        beat.beat_length = fps // beat.bpm
                    elif settings.bpm_up.collidepoint(event.pos):
                        beat.bpm = min(20, beat.bpm + 1)
                        beat.beat_length = fps // beat.bpm
                    elif settings.beats_down.collidepoint(event.pos):
                        beat.beats = max(1, beat.beats - 1)
                        beat.box_w = (WIDTH-LEFT_BOX) // beat.beats
                        for inst in beat.active_boxes:
                            inst.pop()
                    elif settings.beats_up.collidepoint(event.pos):
                        beat.beats = min(20, beat.beats + 1)
                        beat.box_w = (WIDTH-LEFT_BOX) // beat.beats
                        for inst in beat.active_boxes:
                            inst.append(False)
        pygame.display.update()