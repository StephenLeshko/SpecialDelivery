import pygame
pygame.init()

map = """
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

# map = """
# BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# B
# BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
# """

map_split = map.splitlines()
map_split = map_split[1:]
rect_list = []
def build_map(screen):
    bg = pygame.image.load('images/game_bground.png')
    brick = pygame.image.load('images/brick.png').convert()

    screen.blit(bg, (0, 0))
    for y, line in enumerate(map_split):
        for x, char in enumerate(line):
            if char == 'B':
                new_brick = brick
                rect = new_brick.get_rect(topleft=(x * 30, y * 30))
                rect_list.append(rect)
                screen.blit(brick, rect)
    pygame.image.save(screen, 'map.png')
    return True
