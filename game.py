import pygame 
from sys import exit
from random import randint, choice
import map_maker as mm


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


#important variables



#functions

def update():
    pass

#all the bliting takes place here
def draw():
    screen.blit(game_bground, (0, 0))
    screen.blit(car, (car_x, car_y))
    # screen.blit(brick, (0,0))
    # screen.blit(brick, (30, 0))
    # screen.blit()
do = True


mm.build_map(screen)
game_bground = pygame.image.load('map.png').convert()
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
    

