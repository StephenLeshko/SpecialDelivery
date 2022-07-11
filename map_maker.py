from distutils.command import build
import pygame
import random
pygame.init()


#ex: 'b2' : {'edges' : ['b4', 'd2'], 'walls': ['b3', 'c2']}
def build_graph(width, height):
    graph = {}
    for row in range(height):
        for col in range(width):
            letter_val = 65 + row
            node = create_code(letter_val, col)
            if row % 2 == 1 and col % 2 == 1: #both odd numbers, can add to graph
                edges = []
                walls = []
                #add both the edges and walls simultanously
                if row > 1: 
                    edges.append(create_code(letter_val - 2, col))
                    walls.append(create_code(letter_val - 1, col))
                if col > 1: 
                    edges.append(create_code(letter_val, col - 2))
                    walls.append(create_code(letter_val, col - 1))
                if row < height - 2: 
                    edges.append(create_code(letter_val + 2, col))
                    walls.append(create_code(letter_val + 1, col))
                if col < width - 2: 
                    edges.append(create_code(letter_val, col + 2))
                    walls.append(create_code(letter_val, col + 1))
                dict = {}
                dict['edges'] = edges
                dict['walls'] = walls
                graph[node] = dict
    return graph

def depth_search_maze(graph):
    remove_walls = set([]) #what gets returned
    visited = set([])
    stack = []
    wall_stack = []
    stack.append('B2')
    while len(stack) > 0:
        cur = stack.pop()
        cur_wall = None
        if len(wall_stack) > 0:
            cur_wall = wall_stack.pop()
        if cur not in visited:
            visited.add(cur)
            remove_walls.add(cur_wall)
            #randomly inspect each of the neighbors
            edge_num = len(graph[cur]['edges'])
            ran_list = random.sample(range(0, edge_num), edge_num)
            for i in range(edge_num):
                edge = graph[cur]['edges'][ran_list[i]]                    
                if edge not in visited:
                    stack.append(edge)
                    wall = graph[cur]['walls'][ran_list[i]]
                    wall_stack.append(wall)

    return remove_walls

def create_code(letter_val, num):
    return str(chr(letter_val)) + str(num + 1)

def clear_map():
    global rect_list
    rect_list = []

def prepare_map(game_map):
    game_map = game_map.splitlines()
    return game_map[1:]

def map_string(width, height):
    string = '\n'
    for i in range(height):
        if i % 2 == 0:
            added = width * 'B'
            string += added
            string += '\n'
        else:
            for j in range(width):
                if j % 2 == 0:
                    string += 'B'
                else: string += ' '
            string += '\n'
    return string


#just for creating a map image & saving the rects
def build_map(screen):
    clear_map()
    bg = pygame.image.load('images/game_bground.png')
    brick_single = pygame.image.load('images/brick_sin30.png').convert()
    brick_hor = pygame.image.load('images/brick_hor30.png').convert()
    brick_ver = pygame.image.load('images/brick_ver30.png').convert()
    width, height = 21, 11
    #map selection
    # map = maps[map_num]
    map = prepare_map(map_string(width, height))

    
    removal = depth_search_maze(build_graph(width, height))

    screen.blit(bg, (0, 0))
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            code = create_code(65 + y, x)
            if char == 'B' and code not in removal:
                #coordinates
                x_mult = x // 2
                y_mult = y // 2
            
                if x % 2 == 0 and y % 2 == 0: #singular brick
                    rect = brick_single.get_rect(topleft=(x_mult * 120, y_mult * 120))
                    rect_list.append(rect)
                    screen.blit(brick_single, rect)
                    
                elif x % 2 == 1: #horizontal
                    rect = brick_hor.get_rect(topleft=(x_mult * 120 + 30, y_mult * 120))
                    rect_list.append(rect)
                    screen.blit(brick_hor, rect)
                else: #vertical
                    rect = brick_ver.get_rect(topleft=(x_mult * 120, y_mult * 120 + 30))
                    rect_list.append(rect)
                    screen.blit(brick_ver, rect) 
    pygame.image.save(screen, 'map.png')
    return True
