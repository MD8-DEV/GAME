import pygame
from player import Player
from block import load_stage
from stage import mystage

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Game")
clock = pygame.time.Clock()

stage = mystage


player_group = pygame.sprite.GroupSingle(Player())

blocks,levers,doors,inputs,main = load_stage(stage)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((31, 35, 47))
    player_group.draw(screen)
    blocks.draw(screen)
    levers.draw(screen)
    doors.draw(screen)
    # pygame.draw.rect(screen, 'red', player_group.sprite.collide_rect_right)
    # pygame.draw.rect(screen, 'blue', player_group.sprite.collide_rect_left)
    # pygame.draw.rect(screen, 'green', player_group.sprite.collide_rect_up)
    # pygame.draw.rect(screen, 'yellow', player_group.sprite.collide_rect_down)
    blocks.update()
    levers.update(player_group.sprite, events)
    doors.update(inputs)
    player_group.update(main)
    pygame.display.update()
    clock.tick(65)
