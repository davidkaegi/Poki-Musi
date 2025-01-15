import random

import hardware

import music

def run(hw):

    bg_music = music.MusicPlayer('Music/Sokoban_Theme.mid', hw)

    wall=0
    floor=1
    target=2
    box=3
    boxTgt=4
    player=5

    background=[[wall] * 16 for _ in range(12)]

    for i in range(10):
        for j in range(14):
            background[i+1][j+1]=floor

    game_board = [[0] * 16 for _ in range(12)]

    for i in range(12):
        for j in range(16):
            game_board[i][j]=background[i][j]

    def soko_boardToPixel():
        for i in range(12):
            for j in range(16):
                here=game_board[i][j]
                if here == wall:
                    hw.pixel[i][j] = (0.1, 0.1, 0.1) 
                elif here == floor:
                    hw.pixel[i][j] = (0, 0, 0) 
                elif here == target:
                    hw.pixel[i][j] = (1, 0.2, 0) 
                elif here == box:
                    hw.pixel[i][j] = (0, 1, 0) 
                elif here == boxTgt:
                    hw.pixel[i][j] = (0, 0.1, 0) 
                elif here == player:
                    hw.pixel[i][j] = (0.1, 0.1, 1.0)  
                else:
                    hw.pixel[i][j] = (0, 0, 0)
                #black *should never be shown

    def check_box(i,j,push_i,push_j):
        if game_board[i+push_i][j+push_j] == floor:
            game_board[i+push_i][j+push_j] = box
            game_board[i][j] = background[i][j]
            return True
        elif game_board[i+push_i][j+push_j] == target:
            game_board[i+push_i][j+push_j] = boxTgt
            game_board[i][j] = background[i][j]
            return True
        else:
            return False

    def check_collision(i,j,push_i,push_j):
        if game_board[i+push_i][j+push_j] == floor:
            return True
        elif game_board[i+push_i][j+push_j] == target:
            return True
        elif game_board[i+push_i][j+push_j] == wall:
            return False
        elif game_board[i+push_i][j+push_j] == box:
            return check_box(i+push_i,j+push_j,push_i,push_j)
        elif game_board[i+push_i][j+push_j] == boxTgt:
            return check_box(i+push_i,j+push_j,push_i,push_j)
        else:
            return False

    def isWin():
        for i in range(12):
            for j in range(16):
                if background[i][j] == target:
                    if game_board[i][j]!=boxTgt:
                        return False
        return True
    
    player_i = 0
    player_j = 0

    def load_level(path):
        nonlocal player_i, player_j

        file = open(path, 'r')
        
        input_lines = []
        line = file.readline()
        while len(line) > 0:
            input_lines.append(line.replace('\n', ''))
            line = file.readline()

        for c in range(16):
            for r in range(12):
                background[r][c] = floor
                game_board[r][c] = floor
        
        w = max([len(line) for line in input_lines])
        h = len(input_lines)

        begin_c = int(round((16 - w) / 2))
        begin_r = int(round((12 - h) / 2))
        for x in range(w):
            for y in range(h):
                char = input_lines[y][x] if x < len(input_lines[y]) else ' '
                if char == ' ':
                    background[begin_r + y][begin_c + x] = floor
                    game_board[begin_r + y][begin_c + x] = floor
                elif char == '#':
                    background[begin_r + y][begin_c + x] = wall 
                    game_board[begin_r + y][begin_c + x] = wall 
                elif char == '.':
                    background[begin_r + y][begin_c + x] = target 
                    game_board[begin_r + y][begin_c + x] = target 
                elif char == '$':
                    game_board[begin_r + y][begin_c + x] = box 
                elif char == '@':
                    game_board[begin_r + y][begin_c + x] = player 
                    player_i = begin_r + y
                    player_j = begin_c + x
                elif char == '*':
                    background[begin_r + y][begin_c + x] = target
                    game_board[begin_r + y][begin_c + x] = boxTgt

        pass

    #this matters
    lockout=0
    max_lockout=10
    #lockout prevents multiple inputs in short succession

    curr_level = 0
    n_levels = 9

    load_level('sokoban_levels/' + str(curr_level) + '.txt')

    while True:

        if hw.is_key_down(hardware.KEY_RESET):
            load_level('sokoban_levels/' + str(curr_level) + '.txt')

        if lockout == 0:

            if hw.is_key_down(hardware.KEY_SKIP):
                curr_level += 1
                load_level('sokoban_levels/' + str(curr_level) + '.txt')
                lockout=max_lockout #If we don't lockout it skips 10 levels

            if hw.is_key_down(hardware.KEY_UP):

                if check_collision(player_i,player_j,-1,0):
                    game_board[player_i][player_j]=background[player_i][player_j]	
                    player_i-=1
                    game_board[player_i][player_j]=player
                    hw.click(2)
                #maybe play a bonk sound (else)
                lockout=max_lockout

            elif hw.is_key_down(hardware.KEY_DOWN):

                if check_collision(player_i,player_j,1,0):
                    game_board[player_i][player_j]=background[player_i][player_j]
                    player_i+=1
                    game_board[player_i][player_j]=player
                    hw.click(2)
                lockout=max_lockout

            elif hw.is_key_down(hardware.KEY_LEFT):

                if check_collision(player_i,player_j,0,-1):
                    game_board[player_i][player_j]=background[player_i][player_j]
                    player_j-=1
                    game_board[player_i][player_j]=player
                    hw.click(2)
                lockout=max_lockout

            elif hw.is_key_down(hardware.KEY_RIGHT):
                if check_collision(player_i,player_j,0,1):
                    game_board[player_i][player_j]=background[player_i][player_j]
                    player_j+=1
                    game_board[player_i][player_j]=player
                    hw.click(2)
                lockout=max_lockout

        else:
            if lockout > 0:
                lockout-=1
        
        if hw.is_key_down(hardware.KEY_ESCAPE):
            for i in range(3):
                hw.note_off(i)
            break

        soko_boardToPixel()

        if isWin():
            curr_level += 1
            curr_level %= n_levels
            load_level('sokoban_levels/' + str(curr_level) + '.txt')
            hw.note_on(2, 55, 0.5)

        bg_music.tick()
        hw.refresh()
    return curr_level
