from distutils.command import build
import pygame
import random
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
map_num = 2

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
            # first = True
            for i in range(edge_num):
                edge = graph[cur]['edges'][ran_list[i]]                    
                if edge not in visited:
                    stack.append(edge)
                    wall = graph[cur]['walls'][ran_list[i]]
                    wall_stack.append(wall)
                    # if first:
                    #     remove_walls.add(wall_stack.pop())
                    #     first = False
    return remove_walls

def create_code(letter_val, num):
    return str(chr(letter_val)) + str(num + 1)
# print(build_graph(7, 7))


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
    width, height = 41, 21
    #map selection
    map = maps[map_num]
    map = prepare_map(map)

    
    removal = depth_search_maze(build_graph(width, height))

    screen.blit(bg, (0, 0))
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            code = create_code(65 + y, x)
            if char == 'B' and code not in removal:
                new_brick = brick
                rect = new_brick.get_rect(topleft=(x * 30, y * 30))
                rect_list.append(rect)
                screen.blit(brick, rect)
    pygame.image.save(screen, 'map.png')
    # map_num += 1
    return True
