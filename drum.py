import json
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
    
    def __init__(self, beats = 16, bpm = 5, instruments = 6, active_boxes = None, name = None):
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
        self.name = name
        mixer.set_num_channels(3*self.instruments)

    def update(self):
        '''
            Updates the state of the beat every frame and draws the grid with
            the notes
        '''
        if self.beat_changed:
            self.play_notes()
            self.beat_changed = False
        if self.playing:
            self.draw_grid()
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
        self.bpm_down = None
        self.bpm_up = None
        self.beats_down = None
        self.beats_up = None
        self.name_save = ''
        self.label_font = label_font
        self.action = 'play'

    def draw(self):
        if self.action =='play':
            self.draw_play()
        elif self.action == 'save':
            self.draw_save()
        elif self.action == 'load':
            self.draw_load()

    def draw_play(self):
        '''
            Draws the current settings and the options to increment or decrement
                * BPM
                * Beats on screen
                * Save button
                * Load button
        '''

        #BPM
        bpm_text = self.label_font.render('BPM', True, WHITE)
        screen.blit(bpm_text, (100, HEIGHT - BOTTOM_BOX + 40))
        bpm_up_text = self.label_font.render('+', True, WHITE)
        screen.blit(bpm_up_text, (243, HEIGHT - BOTTOM_BOX + 82))
        bpm_down_text = self.label_font.render('-', True, WHITE)
        screen.blit(bpm_down_text, (120, HEIGHT - BOTTOM_BOX + 82))
        bpm_counter_text = self.label_font.render(str(self.beat.bpm), True, WHITE)
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
        beats_text = self.label_font.render('Beats', True, WHITE)
        screen.blit(beats_text, (400, HEIGHT - BOTTOM_BOX + 40))
        beats_up_text = self.label_font.render('+', True, WHITE)
        screen.blit(beats_up_text, (543, HEIGHT - BOTTOM_BOX + 82))
        beats_down_text = self.label_font.render('-', True, WHITE)
        screen.blit(beats_down_text, (420, HEIGHT - BOTTOM_BOX + 82))
        beats_counter_text = self.label_font.render(str(self.beat.beats), True, WHITE)
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

        #Save beat
        save_text = self.label_font.render('Save Beat', True, WHITE)
        screen.blit(save_text, (700, HEIGHT - BOTTOM_BOX + 80))
        pygame.draw.rect(screen, BLACK,
        [696, HEIGHT - BOTTOM_BOX + 73, 154, 54], 2, 5)
        self.save_button = pygame.draw.rect(screen, GREEN,
            [698, HEIGHT - BOTTOM_BOX + 75, 150, 50], 1, 5)

        #Load Beat
        load_text = self.label_font.render('Load Beat', True, WHITE)
        screen.blit(load_text, (1000, HEIGHT - BOTTOM_BOX + 80))
        self.load_button = pygame.draw.rect(screen, BLACK,
        [996, HEIGHT - BOTTOM_BOX + 73, 154, 54], 2, 5)
        pygame.draw.rect(screen, GREEN,
            [998, HEIGHT - BOTTOM_BOX + 75, 150, 50], 1, 5)

    def draw_save(self):
        self.bpm_down = pygame.draw.rect(screen, BLACK, [-1, 0, 0, 0])
        self.bpm_up = pygame.draw.rect(screen, BLACK, [-1, 0, 0, 0])
        self.beats_down = pygame.draw.rect(screen, BLACK, [-1, 0, 0, 0])
        self.beats_up = pygame.draw.rect(screen, BLACK, [-1, 0, 0, 0])
        save_text = big_label_font.render('Save', True, WHITE)
        screen.blit(save_text, ((WIDTH // 2) - 100, 200))
        pygame.draw.rect(screen, GREEN, [(WIDTH // 2) - 500, 300, 1000, 100], 3, 5)
        save_name_text = big_label_font.render(self.name_save, True, WHITE)
        screen.blit(save_name_text, ((WIDTH // 2) - 450, 314))

    def draw_load(self):
        pass

    def save_beat(self):
        with open('saved_beats.json', 'r+') as file:
            beats_saved = json.load(file)
            beats_saved[self.name_save] = self.beat.active_boxes
        with open('saved_beats.json', 'w+') as file:
            json.dump(beats_saved, file, indent=4)
        self.name_save = ''
        pygame.key.stop_text_input()
        self.beat.playing = True
        self.action = 'play'

    def load_beat(self):
        pass


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


def validate_saved_file():
    if os.path.exists("saved_beats.json"):
        return
    try:
        with open("saved_beats.json", "w+") as saved:
            saved.write("{}")
        return
    except:
        print("Exception when creating the file for saved beats")
        exit()


if __name__ == '__main__':
    validate_font(font_name)
    validate_saved_file()
    label_font = pygame.font.Font(font_name, 32)
    big_label_font = pygame.font.Font(font_name, 72)
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
                        event.pos[1] < HEIGHT-BOTTOM_BOX and beat.playing:
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
                    elif settings.load_button.collidepoint(event.pos):
                        beat.playing = False
                        settings.action = 'load'
                    elif settings.save_button.collidepoint(event.pos):
                        beat.playing = False
                        pygame.key.start_text_input()
                        name_savePos = 0
                        settings.action = 'save'
            elif event.type == pygame.KEYDOWN:
                if settings.action == 'save':
                    if event.key == pygame.K_BACKSPACE:
                        if (len(settings.name_save) > 0 and name_savePos > 0):
                            settings.name_save = settings.name_save[0:name_savePos-1] + settings.name_save[name_savePos:]
                            name_savePos = max(0,name_savePos-1)
                            
                    elif event.key == pygame.K_DELETE:
                        settings.name_save = settings.name_save[0:name_savePos] + settings.name_save[name_savePos+1:]
                    elif event.key == pygame.K_LEFT:
                        name_savePos = max(0,name_savePos-1)
                    elif event.key == pygame.K_RIGHT:
                        name_savePos = min(len(settings.name_save),name_savePos+1)
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        settings.save_beat()
            elif event.type == pygame.TEXTINPUT:
                settings.name_save = settings.name_save[0:name_savePos] + event.text + settings.name_save[name_savePos:]
                name_savePos += 1

        pygame.display.update()