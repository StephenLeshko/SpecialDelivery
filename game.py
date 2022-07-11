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

#sounds

#background images
game_bground = pygame.image.load('images/game_bground.png').convert()
load_screen = pygame.image.load('images/load_screen.png').convert()
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
car_vx, car_vy = 0, 0
car_rect = car.get_rect(center=(42, 42))
score = 0

#customer 
customer_1 = pygame.image.load('images/customer_1.png').convert_alpha()
customer_2 = pygame.image.load('images/customer_2.png').convert_alpha()
customer_3 = pygame.image.load('images/customer_3.png').convert_alpha()
customer_4 = pygame.image.load('images/customer_2.png').convert_alpha()
customers = [customer_1, customer_2, customer_3, customer_4]
customer_index = 0.0
customer = customers[0]
customer_rect = customer.get_rect(topleft=(1112, 510))

#game text
font_big = pygame.font.Font('freesansbold.ttf', 70)
font_med = pygame.font.Font('freesansbold.ttf', 35)
font_sma = pygame.font.Font('freesansbold.ttf', 25)

space_begin = font_med.render('Press Space to Begin', True, (0, 255, 255))
controls = font_sma.render('Voice Controls: Go, Stop, Right, Left, Up, Down', True, (100, 255, 255))
score_hud = font_big.render(f'Score: {score}', True, (240, 240, 10))

space_rect = space_begin.get_rect(center = (850, 450))
controls_rect = controls.get_rect(center = (850, 500))
second_counter = 120
time_hud = font_med.render(f'Time: {second_counter}', True, (240, 8, 0))
time_remain = 20


#important variables
direction = 'down'
moving = False
directions = ['up', 'down', 'left', 'right']
game_active = False

#functions
def animate_cars():
    global car_index, cars, car
    car_index += 0.2
    if car_index > 4:
        car_index = 0
    car = cars[int(car_index)]

def animate_customer():
    global customer_index, customers, customer
    customer_index += 0.3
    if customer_index > 3:
        customer_index = 0
    customer = customers[int(customer_index)]

def check_collision():
    
    if len(mm.rect_list) != 0:
        for rect in mm.rect_list:
            if pygame.Rect.colliderect(car_rect, rect):
                # print('collision')
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
        elif word != 'no' or word != 'yes':
            moving = True
            direction = word
        vc.kill_audio()
        vc.frames.clear()
        vc.making_file = False
        return True
    return False
    
def drop_time():
    global time_remain, second_counter
    time_remain -= 1
    if time_remain == 0:
        time_remain = 20
        second_counter -= 1
    if second_counter == 0:
        game_over()

def reset_time():
    global time_remain, second_counter
    time_remain = 20
    second_counter = 120


def game_over():
    global game_active, car_rect, moving, direction, score_hud
    game_active = False
    fail_sound = pygame.mixer.Sound('fail.wav')
    fail_sound.set_volume(1)
    fail_sound.play()
    car_rect.x, car_rect.y = 45, 30
    moving = False
    direction = 'down'
    score_hud = font_big.render(f'Score: {score}', True, (240, 240, 10))
    reset_time()
    new_map()


def new_map():
    global game_bground
    mm.build_map(screen)
    game_bground = pygame.image.load('map.png').convert()

def update():
    global car_vx, car_vy, car, car_rect, moving, time_hud
    animate_customer()
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
    
    #check collision
    elif check_collision():
        car_rect.x -= (2 * car_vx)
        car_rect.y -= (2 * car_vy)
        moving = False
    if moving == False:
        car_vx = 0
        car_vy = 0
    car_rect.x += car_vx
    car_rect.y += car_vy
    
    drop_time()
    time_hud = font_med.render(f'Time: {second_counter}', True, (240, 8, 0))
    win()

    
def win():
    global car_rect, moving, direction, score
    if pygame.Rect.colliderect(car_rect, customer_rect):
        coin = pygame.mixer.Sound('coin.wav')
        coin.set_volume(1)
        coin.play()
        #record score, set to HUD
        #turn off the game
        direction = 'down'
        moving = False
        car_rect.x, car_rect.y = 45, 30
        score += (second_counter) * 50
        reset_time()
        new_map()

#all the bliting takes place here
def draw():
    screen.blit(game_bground, (0, 0))
    screen.blit(car, car_rect)
    screen.blit(customer, customer_rect)
    screen.blit(time_hud, (1000, 40))

mm.build_map(screen)
game_bground = pygame.image.load('map.png').convert()

#theme musics
# bg_music = pygame.mixer.Sound('theme.wav')
# bg_music.set_volume(0.2)
# bg_music.play(loops=-1)

#audio setup

space_duration = 50
space_count = 0

#---MAIN LOOP---
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score = 0
    #draw & update cycle
    if game_active:
        update()
        draw()
    else:
        space_count += 1
        screen.blit(load_screen, (0, 0))
        if space_count > (space_duration / 2):
            screen.blit(space_begin, space_rect)
        if space_count == space_duration:
            space_count = 0
        screen.blit(score_hud, (550, 200))
        screen.blit(controls, controls_rect)
    
    pygame.display.update()
    #usually at 60... what does it actually run at
    clock.tick(20) #4.37 seconds at 90
