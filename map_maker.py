import pygame
pygame.init()

map1 = """
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B  B            B       B     B        B
B  B     B      B       B     B        B
B  B     BBBBB  B  BBB  B  B  B  B     B
B  B         B  B  B B  B  B  B  B     B
B  B         B     B B     B  B  B     B
B  BBBBBBB   B     B B     B     B     B
B            B  B  BBBBBBBBBBBBBBB     B
B            B  B             B        B
BBBB  BBBBBBBB  B      B      B        B
B  B  B         B      B      B     BBBB
B  B  B         B      B               B
BBBB  BBB  BBBBBB   B  BBBBBBBB   BBBBBB            
B       B  B        B  B      B        B
B       B  B        B  B BBB  B  BBB   B
B  BBBBBB      BBBBBB  B B B  B  BBB   B
B  B           B    B  B B B  B        B
B  BB  BB  BBBBB  B BBBB B B  BBBBBB   B
B      B          B      B B           B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
"""

map2 = """
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
"""

map3 = """
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
B B B B B B B B B B B B B B B B B B B B B
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
"""



#Last thing to implement: Random Maze Generation....
maps = [map1, map2, map3]
map_num = 0

# map_split = map.splitlines()
# map_split = map_split[1:]
# rect_list = []

def clear_map():
    global rect_list
    rect_list = []

def prepare_map(game_map):
    game_map = game_map.splitlines()
    return game_map[1:]

#just for creating a map image & saving the rects
def build_map(screen):
    global map_num
    clear_map()
    bg = pygame.image.load('images/game_bground.png')
    brick = pygame.image.load('images/brick.png').convert()

    #map selection
    map = maps[map_num]
    map = prepare_map(map)

    screen.blit(bg, (0, 0))
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == 'B':
                new_brick = brick
                rect = new_brick.get_rect(topleft=(x * 30, y * 30))
                rect_list.append(rect)
                screen.blit(brick, rect)
    pygame.image.save(screen, 'map.png')
    map_num += 1
    return True
