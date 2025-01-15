# Poki Musi

## Description
Poki Musi is a retro game console with the ability to play 3 classic games: Snake, Tetris and Sokoban.
The hardware of the console of the console consisted of of a raspberry pi connected to a custom-built 12x16 grid of LEDs.
This repository contains the software aspect of the project.

## Instructions
In order to experience the Poki Musi on other hardware, the Pygame library is used to display the graphics that would be shown on the rasberry pi.
To run use the "console" the user must run the menu.py file found in this repository. The program will then open the game selection menu. The keyboard controls are as follows:
<ul>
<li>Up and Down arrows are used to navigate between games</li>
<li>Right arrow is open the selected game</li>
</ul>
When each game is selected, an image depicting that game will appear on screen. In case the images are unclear, the games appear in this order:
<ol>
<li>Snake</li>
<li>Tetris</li>
<li>Sokoban</li>
</ol>
Once a game is opened, every game is controlled using the arrow keys and can be exited by pressing <strong>esc</strong>.
Note that tertris was designed to be played with the console rotated 90 degrees, and thus, the graphics will appear rotated by 90 degrees.
