import hardware
import snake_hw
import tetris_hw
import sokoban

hw = hardware.get_hardware(True)

#colour values (change these if you need)
R=(1,0,0)#red
G=(0,1,0)#green
B=(0,0,1)#blue
Y=(1,1,0)#yellow
O=(1,0.5,0)#blue
C=(0,1,1)#cyan
P=(0.5,0,1)#purple, this one may need to change, but I was running low on colours
W=(0.2, 0.2, 0.2)#Sokoban Wall


(0,0,0)
(  G  )


#I could not come up with something smarter than manually entering the art
snake = [
[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
[(0,0,0),(  G  ),(  G  ),(0,0,0),(0,0,0),(  R  ),(0,0,0),(0,0,0)],
[(0,0,0),(  G  ),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
[(0,0,0),(  G  ),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
[(0,0,0),(  G  ),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
[(0,0,0),(  G  ),(  G  ),(  G  ),(  G  ),(  G  ),(  G  ),(0,0,0)],
[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(  G  ),(0,0,0)],
[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
]

tetris = [
[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(  Y  ),(0,0,0)],
[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(  Y  ),(  Y  ),(0,0,0)],
[(  P  ),(  P  ),(  P  ),(  P  ),(0,0,0),(0,0,0),(  Y  ),(0,0,0)],
[(  G  ),(  G  ),(  O  ),(  R  ),(  R  ),(0,0,0),(0,0,0),(0,0,0)],
[(  G  ),(  O  ),(  O  ),(  R  ),(  R  ),(  B  ),(0,0,0),(0,0,0)],
[(  G  ),(  O  ),(  C  ),(  C  ),(  C  ),(  B  ),(  B  ),(0,0,0)],
[(  R  ),(  R  ),(  C  ),(  Y  ),(  O  ),(  O  ),(  B  ),(0,0,0)],
[(  R  ),(  R  ),(  Y  ),(  Y  ),(  Y  ),(  O  ),(  O  ),(0,0,0)],
]

copy = [
[(  W  ),(  W  ),(  W  ),(  W  ),(  W  ),(  W  ),(  W  ),(  W  )],
[(  W  ),(  B  ),(0,0,0),(  G  ),(0,0,0),(0,0,0),(  R  ),(  W  )],
[(  W  ),(  W  ),(  W  ),(0,0,0),(0,0,0),(0,0,0),(  W  ),(  W  )],
[(  W  ),(  R  ),(  W  ),(  W  ),(0,0,0),(0,0,0),(  W  ),(  W  )],
[(  W  ),(0,0,0),(  W  ),(0,0,0),(0,0,0),(0,0,0),(  W  ),(  W  )],
[(  W  ),(  G  ),(0,0,0),(0,0,0),(  G  ),(0,0,0),(0,0,0),(  W  )],
[(  W  ),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(  R  ),(  W  )],
[(  W  ),(  W  ),(  W  ),(  W  ),(  W  ),(  W  ),(  W  ),(  W  )],
]

trophy = [
    [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(0,0,0)],
    [(0,0,0),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(0,0,0)],
    [(0,0,0),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(0,0,0)],
    [(0,0,0),(0,0,0),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(  Y  ),(  Y  ),(  Y  ),(  Y  ),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(0,0,0),(  Y  ),(  Y  ),(0,0,0),(0,0,0),(0,0,0)],
    [(0,0,0),(0,0,0),(  O  ),(  O  ),(  O  ),(  O  ),(0,0,0),(0,0,0)],
]

def draw_square(i,j,size,colour):
    for di in range(size):
        for dj in range(size):
            hw.pixel[i+di][j+dj]=colour

def draw_initial(state):
    for i in range(12):
        for j in range(16):
            hw.pixel[i][j]=(0,0,0)

    draw_square(1,1,2,(0.5,0.5,0.5))
    draw_square(5,1,2,(0.5,0.5,0.5))
    draw_square(9,1,2,(0.5,0.5,0.5))
    if state == 0:
        draw_square(1,1,2,(1,1,1))
    elif state == 1:
        draw_square(5,1,2,(1,1,1))
    elif state == 2:
        draw_square(9,1,2,(1,1,1))

    draw_icon(state)

def draw_icon(state):
    draw_square(1,5,10,(0.5*state,0,0.5))
    if state == 0:
        arr=snake
    elif state == 1:
        arr=tetris
    elif state == 2:
        arr=copy
    else:
        arr=trophy
    for i in range(8):
        for j in range(8):
            hw.pixel[2+i][6+j]=arr[i][j]

def draw_trophy():
    for i in range(8):
        for j in range(8):
            hw.pixel[2+i][6+j]=trophy[i][j]

lockout=0
max_lockout=10
game_choice=0
draw_initial(0)
#lockout prevents multiple inputs in short succession

def beep():

    hw.note_on(0, 110, 0.09)
    hw.note_on(1, 220, 0.07)
    hw.note_on(2, 440, 0.05)

snake_hi=0
tetris_hi=0
sokoban_hi=0

score=0

while True:

    if lockout == 0:
        if hw.is_key_down(hardware.KEY_UP):
            if game_choice != 0:
                draw_square(1+4*game_choice,1,2,(0.5,0.5,0.5))
                game_choice-=1
                draw_square(1+4*game_choice,1,2,(1,1,1))
                draw_icon(game_choice)
                beep()
                lockout=max_lockout
        elif hw.is_key_down(hardware.KEY_DOWN):
            if game_choice != 2:
                draw_square(1+4*game_choice,1,2,(0.5,0.5,0.5))
                game_choice+=1
                draw_square(1+4*game_choice,1,2,(1,1,1))
                draw_icon(game_choice)
                beep()
                lockout=max_lockout
        elif hw.is_key_down(hardware.KEY_RIGHT):
            #temporary game enter until more key are added
            if game_choice == 0:
                #snake
                score=snake_hw.run(hw)
                if score > snake_hi:
                    snake_hi=score
                    draw_initial(game_choice)
                    draw_trophy()
                    for i in range(50):
                        hw.refresh()
                draw_initial(game_choice)
            
            if game_choice == 1:
                tetris_hw.run(hw)
                draw_initial(game_choice)
                lockout=50

            if game_choice == 2:
                score=sokoban.run(hw)
                if score > tetris_hi:
                    sokoban_hi=score
                    draw_initial(game_choice)
                    draw_trophy()
                    for i in range(50):
                        hw.refresh()
                draw_initial(game_choice)
                lockout=50

    else:
        if lockout > 0:
            lockout-=1

    hw.refresh()
