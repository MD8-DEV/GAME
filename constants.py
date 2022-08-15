import pygame

# from block import Block, LeverBlock

def load_animation(file, width, height, len):
    surface = pygame.image.load(file) if type(file) != pygame.surface.Surface else file
    h = int(height / len)
    result = []
    for i in range(len):
        result.append(surface.subsurface((0,i*h,width,h)))
    return result

temp = []
BLOCKS = []

for i in load_animation('./assets/industrial.v1.png',512,512,32):
    for x in load_animation(pygame.transform.rotate(i,-90),16,512,32):
        temp.append(pygame.transform.scale(pygame.transform.rotate(x,90),(2*16,2*16)))
    BLOCKS.append(temp)
    temp = []

scale = 2

player_scale = 1

IDLE = [pygame.transform.scale(x,(player_scale*16,player_scale*16)) for x in BLOCKS[16][:4]]
RUN = [pygame.transform.scale(x,(player_scale*16,player_scale*16)) for x in  BLOCKS[17][:4]]
JUMP = [pygame.transform.scale(x,(player_scale*16,player_scale*16)) for x in  BLOCKS[17][4:6]]
FALL = [pygame.transform.scale(x,(player_scale*16,player_scale*16)) for x in BLOCKS[17][6:7]]

BLOCKS_DICT = {
    'X':[(0,13),0,0,0],
    'L':[(8,1),(0,0,16,10),0,0],
    'M':[(6,1),(4,1,8,11),0,0],
    'V':[(8,5),0,((8,5,8),(8,7,10)),1],
    'F':[(6,0),0,((6,0,4,1),(6,0,4,-1)),2]
    }

BLOCKS_COLORS = {
    'X': 'red',
    'L': 'white',
    'M': 'gray',
    ' ': 'black',
    'V': 'brown',
    'F': "blue"
}

ALL_BLOCKS = {}

for x in BLOCKS_COLORS.keys():
    ALL_BLOCKS[x] = pygame.key.key_code(x)


if __name__ == '__main__':
    s = pygame.display.set_mode((512,512))
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        s.fill('white')
        pygame.display.update()

