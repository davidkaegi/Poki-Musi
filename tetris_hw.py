
import hardware
import random
import math
import music

PIECES = [
    {
        'color': (0.5, 0, 1),
        'tiles': [(0, 0), (-1, 0), (0, -1), (1, 0)],
        'tile_align': True
    },
    {
        'color': (1, 1, 0),
        'tiles': [(-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)],
        'tile_align': False 
    },
    {
        'color': (0, 1, 1),
        'tiles': [(-1.5, -0.5), (-0.5, -0.5), (0.5, -0.5), (1.5, -0.5)],
        'tile_align': False 
    },
    {
        'color': (0, 0, 1),
        'tiles': [(0, 0), (-1, 0), (-1, -1), (1, 0)],
        'tile_align': True
    },
    {
        'color': (1, 0.5, 0),
        'tiles': [(0, 0), (-1, 0), (1, -1), (1, 0)],
        'tile_align': True
    },
    {
        'color': (0, 1, 0),
        'tiles': [(0, 0), (-1, 0), (0, -1), (1, -1)],
        'tile_align': True
    },
    {
        'color': (1, 0, 0),
        'tiles': [(0, 0), (1, 0), (0, -1), (-1, -1)],
        'tile_align': True
    }
]

WIDTH = 8
HEIGHT = 16
BOARD_X_OFFSET = (12 - WIDTH) // 2

curr_piece_x = 0
curr_piece_y = 0
curr_piece_tiles = []
curr_piece_color = (0, 0, 0)
board = [[None for y in range(HEIGHT)] for x in range(WIDTH)]
score = 0

ticks = 0

bg_music = None 

def refresh(hw):
    global bg_music
    hw.refresh()
    bg_music.tick()

def pick_piece():
    global curr_piece_x, curr_piece_y, curr_piece_tiles, curr_piece_color
    piece = PIECES[random.randint(0, len(PIECES) - 1)]
    curr_piece_x = WIDTH / 2
    curr_piece_y = 0
    if piece['tile_align']:
        curr_piece_x += 0.5
        curr_piece_y += 0.5
    curr_piece_tiles = piece['tiles']
    curr_piece_color = piece['color']


def reset():
    global ticks, board, score
    pick_piece()
    ticks = 0
    board = [[None for y in range(HEIGHT)] for x in range(WIDTH)]
    score = 0

def set_pixel(hw, x, y, c):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    hw.pixel[BOARD_X_OFFSET + x][y] = c

def render(hw):
    global curr_piece_x, curr_piece_y, curr_piece_tiles, curr_piece_color
    for x in range(WIDTH):
        for y in range(HEIGHT):
            set_pixel(hw, x, y, (0, 0, 0))
            if board[x][y]:
                set_pixel(hw, x, y, board[x][y])

    for tile in curr_piece_tiles:
        tx = math.floor(curr_piece_x + tile[0])
        ty = math.floor(curr_piece_y + tile[1])
        set_pixel(hw, tx, ty, curr_piece_color)
    
def solid(x, y):
    if x < 0 or x >= WIDTH or y >= HEIGHT: 
        return True
    if y < 0:
        return False
    return board[x][y] != None

def is_curr_piece_hit():
    global curr_piece_x, curr_piece_y, curr_piece_tiles 
    for tile in curr_piece_tiles:
        tx = math.floor(curr_piece_x + tile[0])
        ty = math.floor(curr_piece_y + tile[1])
        if solid(tx, ty):
            return True
    return False

def shift_left():
    global curr_piece_x
    curr_piece_x += 1
    if is_curr_piece_hit():
        curr_piece_x -= 1
        return False
    return True

def shift_right():
    global curr_piece_x
    curr_piece_x -= 1
    if is_curr_piece_hit():
        curr_piece_x += 1
        return False
    return True

def wall_kick():
    if not is_curr_piece_hit():
        return True
    if shift_left():
        return True
    if shift_right():
        return True
    return False

def rotate_left():
    global curr_piece_tiles
    curr_piece_tiles = [(-tile[1], tile[0]) for tile in curr_piece_tiles]
    if not wall_kick():
        curr_piece_tiles = [(tile[1], -tile[0]) for tile in curr_piece_tiles]

def rotate_right():
    global curr_piece_tiles
    curr_piece_tiles = [(tile[1], -tile[0]) for tile in curr_piece_tiles]
    if not wall_kick():
        curr_piece_tiles = [(-tile[1], tile[0]) for tile in curr_piece_tiles]

def freeze_piece():
    global curr_piece_x, curr_piece_y, curr_piece_tiles, curr_piece_color
    for tile in curr_piece_tiles:
        tx = math.floor(curr_piece_x + tile[0])
        ty = math.floor(curr_piece_y + tile[1])
        if tx < 0 or tx >= WIDTH or ty < 0 or ty >= HEIGHT:
            continue
        board[tx][ty] = curr_piece_color

def is_line_full(y):
    global board
    for x in range(WIDTH):
        if not board[x][y]:
            return False
    return True

def clear_line(line):
    global board
    for y in range(line - 1, 0, -1):
        for x in range(WIDTH):
            board[x][y + 1] = board[x][y]
    for x in range(WIDTH):
        board[x][0] = None

def death(hw):
    for i in range(WIDTH + HEIGHT):
        for x in range(i + 1):
            y = i - x
            set_pixel(hw, x, y, (0, 0, 0))
        for t in range(3):
            refresh(hw)
    reset()

def run(hw):
    global ticks, curr_piece_x, curr_piece_y, bg_music, score
    bg_music = music.MusicPlayer('Music/Tetris_Theme.mid', hw) 
    reset()

    border_color = (0.25, 0.25, 0.25)
    for y in range(16):
        for x in range(BOARD_X_OFFSET):
            hw.pixel[x][y] = border_color 
        for x in range(BOARD_X_OFFSET + WIDTH, 12):
            hw.pixel[x][y] = border_color 

    prev_left_down = False
    prev_right_down = False
    prev_up_down = False
    prev_down_down = False

    had_inputs_since_last_tick = False

    while True:
        refresh(hw)
        render(hw)

        if hw.is_key_down(hardware.KEY_ESCAPE):
            for c in range(3):
                hw.note_off(c)
            return

        if hw.is_key_down(hardware.KEY_LEFT) and not prev_left_down:
            shift_left()
            had_inputs_since_last_tick = True
        if hw.is_key_down(hardware.KEY_RIGHT) and not prev_right_down:
            shift_right()
            had_inputs_since_last_tick = True
        if hw.is_key_down(hardware.KEY_UP) and not prev_up_down:
            rotate_left()
            had_inputs_since_last_tick = True
        if hw.is_key_down(hardware.KEY_DOWN) and not prev_down_down:
            rotate_right()
            had_inputs_since_last_tick = True

        prev_left_down = hw.is_key_down(hardware.KEY_LEFT)
        prev_right_down = hw.is_key_down(hardware.KEY_RIGHT)
        prev_up_down = hw.is_key_down(hardware.KEY_UP)
        prev_down_down = hw.is_key_down(hardware.KEY_DOWN)

        ticks += 1
        if ticks < 5 + 20 / (0.125 * score + 1):
            continue
        ticks = 0

        curr_piece_y += 1
        if is_curr_piece_hit():
            curr_piece_y -= 1

            if not had_inputs_since_last_tick:
                freeze_piece()
                pick_piece()
                score += 1
                if is_curr_piece_hit():
                    death(hw)
                    continue
        
        had_inputs_since_last_tick = False

        full_lines = [y for y in range(HEIGHT) if is_line_full(y)]
        if len(full_lines) > 0:

            # sweep animation
            for x in range(WIDTH):
                for y in full_lines:
                    set_pixel(hw, x, y, (0, 0, 0))

                for t in range(3):
                    refresh(hw)
            
            # shift everything down
            for y in full_lines:
                clear_line(y)
