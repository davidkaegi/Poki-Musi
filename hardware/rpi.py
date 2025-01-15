
import board
import keyboard
import time
import neopixel
import hardware
import RPi.GPIO as GPIO

strip = neopixel.NeoPixel(board.D21, 12 * 16, brightness=0.1, auto_write=False)

pixel = [[(0,0,0)] * 16 for _ in range(12)]

def brighten(colour):
    return (int(colour[0] * 255), int(colour[1] * 255), int(colour[2] * 255))

prev_frame_time = time.time()

sound_pins = [25, 24, 23]
GPIO.setmode(GPIO.BCM)
for pin in sound_pins:
    GPIO.setup(pin, GPIO.OUT)

sound_pwms = [GPIO.PWM(pin, 110) for pin in sound_pins] 
sound_off_times = [-1] * len(sound_pins) 

def refresh():
    global prev_frame_time
    
    for i in range(12):
        for j in range(16):
            if (11 - i) % 2 == 0:
                idx = (11 - i) * 16 + j
                strip[idx] = brighten(pixel[i][j])
            else:
                idx = (11 - i) * 16 + 15 - j
                strip[idx] = brighten(pixel[i][j])
    strip.show()

    curr_time = time.time()
    time_elapsed = curr_time - prev_frame_time
    prev_frame_time = curr_time

    for channel in range(len(sound_pins)):
        if time.time() > sound_off_times[channel]:
            sound_pwms[channel].stop() 

    #time.sleep(1 / 60)

    time.sleep(max(0.001, 1 / 60 - time_elapsed))

def is_key_down(key):
    if key == hardware.KEY_UP:
        return keyboard.is_pressed('up') 
    elif key == hardware.KEY_RIGHT:
        return keyboard.is_pressed('right') 
    elif key == hardware.KEY_DOWN:
        return keyboard.is_pressed('down') 
    elif key == hardware.KEY_LEFT:
        return keyboard.is_pressed('left') 
    elif key == hardware.KEY_ESCAPE:
        return keyboard.is_pressed('escape') 
    elif key == hardware.KEY_RESET:
        return keyboard.is_pressed('r') 
    elif key == hardware.KEY_SKIP:
        return keyboard.is_pressed('s')
    else:
        return False

def note_on(channel, freq, length = -1):
    sound_pwms[channel].ChangeFrequency(freq)
    sound_pwms[channel].start(50.0)
    if length > 0:
        sound_off_times[channel] = time.time() + length
    else:
        sound_off_times[channel] = time.time() + 10000000.0 

def note_off(channel):
    sound_pwms[channel].stop()

def click(channel):
    note_off(channel)
    for _ in range(40):
        time.sleep(0.0005)
        GPIO.output(sound_pins[channel], GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(sound_pins[channel], GPIO.LOW)
