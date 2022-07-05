import pygame 
from sys import exit
from random import randint, choice

from pyparsing import Word
import map_maker as mm
import voice_control as vc
import audioop


pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Special Delivery')
clock = pygame.time.Clock()
# font = pygame.font.Font('font/Pixeltype.ttf', 50)
#sounds

#background images
game_bground = pygame.image.load('images/game_bground.png').convert()
brick = pygame.image.load('images/brick.png').convert()

#game objects & images
car = pygame.image.load('images/car.png').convert_alpha()
car_x, car_y = 45, 30
car_vx, car_vy = 0, 0


#important variables
direction = 'down'
moving = False
directions = ['up', 'down', 'left', 'right']


#functions


def direction_choose():
    global moving, direction
    data = vc.stream.read(vc.FRAMES_PER_BUFFER)
    rms = audioop.rms(data, 2)
    if rms > 500 or vc.making_file == True:
        vc.making_file = True
        vc.frames.append(data)
        vc.file_count += 1
    if (vc.file_count == vc.RATE/vc.FRAMES_PER_BUFFER or rms < 150) and vc.making_file:
        vc.file_count = 0
        vc.create_audio(vc.frames)
        word = vc.predict_audio('noise.wav')
        print(word)
        if word == 'go':
            moving = True
        elif word == 'stop':
            moving = False
        else:
            direction = word
        vc.kill_audio()
        vc.frames.clear()
        vc.making_file = False
    



def update():
    global car_x, car_y, car_vx, car_vy
    direction_choose()
    if moving:
        if direction == 'right':
            car_vx = 5
            car_vy = 0
        elif direction == 'left':
            car_vx = -5
            car_vy = 0
        elif direction == 'up':
            car_vx = 0
            car_vy = -5
        elif direction == 'down':
            car_vx = 0
            car_vy = 5
    else:
        car_vx = 0
        car_vy = 0
    car_x += car_vx
    car_y += car_vy
    

#all the bliting takes place here
def draw():
    screen.blit(game_bground, (0, 0))
    screen.blit(car, (car_x, car_y))
    # screen.blit(brick, (0,0))
    # screen.blit(brick, (30, 0))
    # screen.blit()


mm.build_map(screen)
game_bground = pygame.image.load('map.png').convert()

#audio setup


#---MAIN LOOP---
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #draw & update cycle
    update()
    draw()
    # if do:
    #     pygame.image.save(screen, 'dog.png')
    #     do = False
    pygame.display.update()
    clock.tick(10)
    

