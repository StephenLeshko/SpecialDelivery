import random
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
                if row > 1: #check if not at top
                    edges.append(create_code(letter_val - 2, col))
                    walls.append(create_code(letter_val - 1, col))
                if col > 1: 
                    edges.append(create_code(letter_val, col - 2))
                    walls.append(create_code(letter_val, col - 1))
                if row < height - 2: #check if not at top
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

def create_code(letter_val, num):
    return str(chr(letter_val)) + str(num + 1)
# print(build_graph(7, 7))

# print(random.choice(range(7)))

def depth_search_maze(graph):
    remove_walls = set([]) #what gets returned
    visited = set([])
    stack = []
    stack.append('B2')
    while len(stack) > 0:
        cur = stack.pop()
        if cur not in visited:
            visited.add(cur)
            #randomly inspect each of the neighbors
            edge_num = len(graph[cur]['edges'])
            ran_list = random.sample(range(0, edge_num), edge_num)
            wall_pres = True
            for i in range(edge_num):
                edge = graph[cur]['edges'][ran_list[i]]                    
                if edge not in visited:
                    stack.append(edge)
                    if wall_pres:
                        wall = graph[cur]['walls'][ran_list[i]]
                        remove_walls.add(wall)
                        # wall_pres = False
    return remove_walls
graph = build_graph(7, 7)
print(graph)
print('removal', depth_search_maze(graph))
