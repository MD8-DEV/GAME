import pygame
from constants import *
from constants import BLOCKS, BLOCKS_DICT


class Block(pygame.sprite.Sprite):

    def __init__(self, block, coords):
        super().__init__()
        self.image = BLOCKS[block[0][0]][block[0][1]]
        self.rect = self.image.get_rect(x=coords[0],y=coords[1])
        self.collide_rect = self.image.get_rect(x=coords[0],y=coords[1])

        if block[1]:
            self.image = pygame.Surface.subsurface(self.image, [x for x in block[1]])
            self.rect = self.image.get_rect(x=coords[0],y=coords[1])

class LeverBlock(pygame.sprite.Sprite):

    def __init__(self, block, coords):
        super().__init__()

        self.image = BLOCKS[block[0][0]][block[0][1]]
        self.rect = self.image.get_rect(x=coords[0],y=coords[1])
        self.collide_rect = self.image.get_rect(width=10, center=self.rect.center)

        self.stop_animation = False
        self.triggered = False

        self.animations = [BLOCKS[x[0]][x[1]:x[2]] for x in block[2]]
        self.animation_index = 0
        self.curr_animation_index = 0
        self.curr_animation = self.animations[self.animation_index]
        self.curr_animation_len = len(self.animations[self.animation_index])

    def animate(self):
        if not self.stop_animation:
            if self.curr_animation_index == self.curr_animation_len - 1:
                self.curr_animation_index == 0
                self.stop_animation == True
            else:
                self.stop_animation = False
                self.curr_animation_index += 1
                self.image = self.curr_animation[self.animation_index]

    def main_func(self, sprite, events):
        temp = self.collide_rect.bottom
        self.collide_rect.height = 10
        self.collide_rect.bottom = temp
        if (sprite.rect.bottom == self.collide_rect.top and self.collide_rect.left <= sprite.rect.centerx <= self.collide_rect.right) or sprite.rect.right == self.collide_rect.left or sprite.rect.left == self.collide_rect.right:
            for i in events:
                if i.type == pygame.KEYDOWN and i.key == pygame.K_z: 
                    self.animations[0], self.animations[1] = self.animations[1], self.animations[0]
                    self.animation_index = 0
                    self.triggered = True if not self.triggered else False
                    return
        self.animation_index = 1

    def update(self, sprite, events):
        self.main_func(sprite, events)
        self.curr_animation_index = 0 if self.animation_index else self.curr_animation_index
        self.curr_animation = self.animations[self.animation_index]
        self.curr_animation_len = len(self.animations[self.animation_index])
        self.animate()

class DoorBlock(pygame.sprite.Sprite):
    def __init__(self, block, coords, trigger_coords):
        super().__init__()

        self.block = block

        self.trig_coords = trigger_coords

        self.image = BLOCKS[block[0][0]][block[0][1]]
        self.rect = self.image.get_rect(x=coords[0],y=coords[1])
        self.collide_rect = self.image.get_rect(width=10, center=self.rect.center)

        self.stop_animation = False
        self.trigger = False
        self.trigger_2 = False


        self.animations = [BLOCKS[x[0]][x[1]:x[2]][::x[3]] for x in block[2]]
        self.animation_index = 0
        self.curr_animation_index = 0
        self.curr_animation = self.animations[self.animation_index]
        self.curr_animation_len = 4

    def animate(self, len1):
        if self.curr_animation_index < len1 - 1:
            self.stop_animation = False
            self.curr_animation_index += 1
            self.image = self.curr_animation[self.curr_animation_index]
    
    def main_func(self):
        self.animation_index = int(self.trigger)
        self.curr_animation_index = -1
        self.curr_animation = self.animations[self.animation_index]
        self.animate(self.curr_animation_len)
        if not self.trigger:
            self.collide_rect = self.image.get_rect(width=10, center=self.rect.center)
        else:
            self.collide_rect = self.image.get_rect(width=10, center=(self.rect.centerx, self.rect.centery - 32))
        
    def update(self,inputs):
        self.trigger = inputs[f"{self.trig_coords[0]},{self.trig_coords[1]}"].triggered
        self.main_func()
        self.curr_animation = self.animations[self.animation_index]
        self.curr_animation_len = len(self.animations[self.animation_index])
        

block_group = pygame.sprite.Group()
lever_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
main_group = pygame.sprite.Group()

classes_list = [Block, LeverBlock, DoorBlock]

groups = [block_group, lever_group, door_group]

inputs = {}
outputs = {}

def load_stage(stage):
    for i in range(len(stage)):
        for x in range(len(stage[0])):
            if stage[i][x] != ' ':
                j = stage[i][x]

                if BLOCKS_DICT[j[0]][3] != 2:
                    curr_block = classes_list[BLOCKS_DICT[j[0]][3]](BLOCKS_DICT[j[0]],(x*scale*16,i*scale*16))
                    groups[BLOCKS_DICT[j[0]][3]].add(curr_block)
                    main_group.add(curr_block)

                else:
                    this_input = j.split('-')[1].split(',')
                    curr_block = classes_list[BLOCKS_DICT[j[0]][3]](BLOCKS_DICT[j[0]],(x*scale*16,i*scale*16),this_input)
                    groups[BLOCKS_DICT[j[0]][3]].add(curr_block)
                    main_group.add(curr_block)

                if BLOCKS_DICT[j[0]][3] == 1:
                    inputs[f"{i},{x}"] = curr_block

    return block_group, lever_group, door_group, inputs, main_group
