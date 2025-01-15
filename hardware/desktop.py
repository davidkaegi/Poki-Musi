
import pygame
from pygame.mixer import Sound
import hardware

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pixel = [[(0,0,0)] * 16 for _ in range(12)]

def brighten(colour):
    return (colour[0] * 255, colour[1] * 255, colour[2] * 255)

clock = pygame.time.Clock()

def refresh():
    for i in range(12):
        for j in range(16):
            pygame.draw.rect(screen,(brighten(pixel[i][j])),(50*j,50*i,50,50))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    clock.tick(60)    


def is_key_down(key):
    keys = pygame.key.get_pressed()
    if key == hardware.KEY_UP:
        return keys[pygame.K_UP]
    elif key == hardware.KEY_RIGHT:
        return keys[pygame.K_RIGHT]
    elif key == hardware.KEY_DOWN:
        return keys[pygame.K_DOWN]
    elif key == hardware.KEY_LEFT:
        return keys[pygame.K_LEFT]
    elif key == hardware.KEY_ESCAPE:
        return keys[pygame.K_ESCAPE]
    elif key == hardware.KEY_RESET:
        return keys[pygame.K_r]
    elif key == hardware.KEY_SKIP:
        return keys[pygame.K_s]
    else:
        return False

import pyaudio 

n_channels = 3
note_periods = [0] * n_channels 
note_timers = [0] * n_channels
note_length = [0] * n_channels

def audio_callback(in_data, frame_count, time_info, status):
    sound_data = [0] * frame_count
    for i in range(frame_count): 
        for channel in range(n_channels):
            if note_timers[channel] < note_periods[channel] / 2:
                sound_data[i] += 20
            note_timers[channel] -= 1
            if note_periods[channel] > 0:
                note_length[channel] -= 1
            if note_timers[channel] < 0:
                note_timers[channel] = note_periods[channel]
            if note_length[channel] == 0:
                note_periods[channel] = 0
    return (bytes(sound_data), pyaudio.paContinue)

audio = pyaudio.PyAudio()
stream = audio.open(format=16,
                    channels=1,
                    rate=44100,
                    output=True,
                    stream_callback=audio_callback,
                    frames_per_buffer=720)

def note_off(channel):
    note_periods[channel] = 0

def note_on(channel, freq, length=-1):
    note_periods[channel] = int(round(44100 / freq))
    note_length[channel] = int(round(length * 44100))

def click(channel):
    note_periods[channel] = 40
    note_length[channel] = 120