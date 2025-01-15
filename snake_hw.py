
import hardware
import random
import music

RIGHT = 1
DOWN = 2
LEFT = 3
UP = 4
APPLE = 5

map = [[0 for c in range(16)] for r in range(12)]

map[3][3] = RIGHT
map[3][4] = RIGHT
map[3][5] = RIGHT

tail_x = 3
tail_y = 3
head_x = 5
head_y = 3

extend_snake = False

def reset():
    global map, tail_x, tail_y, head_x, head_y, extend_snake

    map = [[0 for c in range(16)] for r in range(12)]

    map[3][3] = RIGHT
    map[3][4] = RIGHT
    map[3][5] = RIGHT
    map[5][10] = APPLE 

    tail_x = 3
    tail_y = 3
    head_x = 5
    head_y = 3

    extend_snake = False

def free_was_down(hw,was_down):
    if hw.is_key_down(hardware.KEY_RIGHT) == False:
        was_down[0] = False
    if hw.is_key_down(hardware.KEY_DOWN) == False:
        was_down[1] = False
    if hw.is_key_down(hardware.KEY_LEFT) == False:
        was_down[2] = False
    if hw.is_key_down(hardware.KEY_UP) == False:
        was_down[3] = False

def run(hw):

    global map, tail_x, tail_y, head_x, head_y, extend_snake

    bg_music = music.MusicPlayer('Music/Snake_Music.mid', hw)

    hi_score=0
    score=0

    reset()
    ticks = 0

    was_down=[False,False,False,False]
    input_allowed=True

    while True:

        bg_music.tick()
        hw.refresh()

        for r in range(12):
            for c in range(16):
                color = (0, 0, 0) 
                if map[r][c] in [RIGHT, DOWN, LEFT, UP]:
                    color = (0, 1, 0)
                elif map[r][c] == APPLE:
                    color = (1, 0, 0)
                hw.pixel[r][c] = color

        ticks += 1
        
        if hw.is_key_down(hardware.KEY_RIGHT) and map[head_y][head_x] != LEFT:
            if input_allowed and was_down[0] == False:
                input_allowed=False
                free_was_down(hw,was_down)
                was_down[0]=True
                map[head_y][head_x] = RIGHT
        elif hw.is_key_down(hardware.KEY_DOWN) and map[head_y][head_x] != UP:
            if input_allowed and was_down[1] == False:
                input_allowed=False
                free_was_down(hw,was_down)
                was_down[1]=True
                map[head_y][head_x] = DOWN 
        elif hw.is_key_down(hardware.KEY_LEFT) and map[head_y][head_x] != RIGHT:
            if input_allowed and was_down[2] == False:
                input_allowed=False
                free_was_down(hw,was_down)
                was_down[2]=True
                map[head_y][head_x] = LEFT 
        elif hw.is_key_down(hardware.KEY_UP) and map[head_y][head_x] != DOWN:
            if input_allowed and was_down[3] == False:
                input_allowed=False
                free_was_down(hw,was_down)
                was_down[3]=True
                map[head_y][head_x] = UP 
        if hw.is_key_down(hardware.KEY_ESCAPE):
            for i in range(3):
                hw.note_off(i)
            return hi_score
        if input_allowed:
            free_was_down(hw,was_down)

        if ticks % 6 != 0:
            continue 
        
        input_allowed=True

        if not extend_snake:
            tail_dir = map[tail_y][tail_x]
            map[tail_y][tail_x] = 0
            if tail_dir == RIGHT:
                tail_x += 1
            elif tail_dir == DOWN:
                tail_y += 1
            elif tail_dir == LEFT:
                tail_x -= 1
            elif tail_dir == UP:
                tail_y -= 1
            else:
                print("ERROR!!! tail not a direction")
        extend_snake = False
        
        head_dir = map[head_y][head_x]
        if head_dir == RIGHT:
            head_x += 1
        elif head_dir == DOWN:
            head_y += 1
        elif head_dir == LEFT:
            head_x -= 1
        elif head_dir == UP:
            head_y -= 1
        
        if head_x < 0 or head_x >= 16 or head_y < 0 or head_y >= 12 or (map[head_y][head_x] != 0 and map[head_y][head_x] != APPLE):
            hw.note_on(2, 440, 0.5)
            reset() # bonk
            continue
        
        if map[head_y][head_x] == APPLE:
            score+=1
            if score > hi_score:
                hi_score = score
            extend_snake = True
            while True:
                new_apple_x = random.randint(0, 15)
                new_apple_y = random.randint(0, 11)
                if map[new_apple_y][new_apple_x] == 0:
                    map[new_apple_y][new_apple_x] = APPLE
                    break

        map[head_y][head_x] = head_dir
