from numpy import true_divide
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
car = pygame.image.load('images/car_1.png').convert_alpha()
car = pygame.transform.rotate(car, 180)
#car images
car_1 = pygame.image.load('images/car_1.png').convert_alpha()
car_2 = pygame.image.load('images/car_2.png').convert_alpha()
car_3 = pygame.image.load('images/car_3.png').convert_alpha()
car_4 = pygame.image.load('images/car_4.png').convert_alpha()
car_5 = pygame.image.load('images/car_5.png').convert_alpha()

cars = [car_1, car_2, car_3, car_4, car_5]
car_index = 0.0
car_vx, car_vy = 0, 5
car_rect = car.get_rect(topleft=(45, 30))


#important variables
direction = 'down'
moving = False
directions = ['up', 'down', 'left', 'right']


#functions
def animate_cars():
    global car_index, cars, car
    car_index += 0.2
    if car_index > 4:
        car_index = 0
    car = cars[int(car_index)]

def check_collision():
    if len(mm.rect_list) != 0:
        for rect in mm.rect_list:
            if pygame.Rect.colliderect(car_rect, rect):
                return True
    return False

def direction_choose():
    global moving, direction
    data = vc.stream.read(vc.FRAMES_PER_BUFFER)
    rms = audioop.rms(data, 2)
    if rms > 1000 or vc.making_file == True:
        vc.making_file = True
        vc.frames.append(data)
        vc.file_count += 1
    if (vc.file_count >= vc.RATE/vc.FRAMES_PER_BUFFER or rms < 150) and vc.making_file:
        # if rms < 100:
        #     print('RMS did')
        # elif vc.file_count == 40:
        #     print('file')
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
        return True
    return False
    


def update():
    global car_vx, car_vy, car, car_rect
    if direction_choose():
        if moving:
            animate_cars()
            if direction == 'right':
                car = pygame.transform.rotate(car, 270)
                car_vx = 3.5
                car_vy = 0
            elif direction == 'left':
                car = pygame.transform.rotate(car, 90)
                car_vx = -3.5
                car_vy = 0
            elif direction == 'up':
                car = pygame.transform.rotate(car, 360)
                car_vx = 0
                car_vy = -3.5
            elif direction == 'down':
                car = pygame.transform.rotate(car, 180)
                car_vx = 0
                car_vy = 3.5
        else:
            car_vx = 0
            car_vy = 0
    car_rect.x += car_vx
    car_rect.y += car_vy
    

#all the bliting takes place here
def draw():
    screen.blit(game_bground, (0, 0))
    screen.blit(car, car_rect)
    # screen.blit(brick, (0,0))
    # screen.blit(brick, (30, 0))
    # screen.blit()


mm.build_map(screen)
game_bground = pygame.image.load('map.png').convert()
# bg_music = pygame.mixer.Sound('theme.wav')
# bg_music.set_volume(0.2)
# bg_music.play(loops=-1)
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
    clock.tick(60)
    

