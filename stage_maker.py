import pygame
from constants import BLOCKS_COLORS, ALL_BLOCKS

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Game")
clock = pygame.time.Clock()

stage = [
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
]

rects = []
temp = []
file = open('stage.py','w')
for y in range(len(stage)):
    for x in range(len(stage[0])):
        temp.append(pygame.rect.Rect(x*32,y*32,32,32))
    rects.append(temp)
    temp = []

color = 'white'
v = False
m = 0
n = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print(*stage,sep='\n')
            file.write(f'mystage = {str(stage)}')
            exit()
    for i in rects:
        for x in i:
            if x.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                for z in ALL_BLOCKS:
                    if pygame.key.get_pressed()[ALL_BLOCKS[z]]:
                        if not v:
                            if z != 'F':
                                stage[x[1]//32][x[0]//32] = z
                            else:
                                v = True
                                m = x[0]
                                n = x[1]
                        else:
                            if pygame.key.get_pressed()[ALL_BLOCKS["V"]]:
                                stage[n//32][m//32] = f"F-{x[1]//32},{x[0]//32}"
                                stage[x[1]//32][x[0]//32] = "V"
                                v = False
                        color = BLOCKS_COLORS[z]
                        pygame.draw.rect(screen,color,x)

    pygame.display.update()
    clock.tick(60)