import pygame
from constants import IDLE, RUN, JUMP, FALL

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.animation = IDLE
        self.animation_len = len(IDLE)
        self.animation_index = 0

        self.jumping = False
        self.running = False
        self.falling = False
        self.flip = False

        self.ground = 480
        self.floor = 0
        self.right_limit = 640
        self.left_limit = 0

        self.gravity = 0

        self.image = self.animation[self.animation_index]
        self.rect = self.image.get_rect(bottom=300)

        self.collide_rect_down = self.image.get_rect()
        self.collide_rect_up = self.image.get_rect()
        self.collide_rect_right = self.image.get_rect()
        self.collide_rect_left = self.image.get_rect()

    def animate(self):
        if self.animation_index == self.animation_len - 1:
            self.animation_index = 0
        self.animation_index += .2 if self.animation != IDLE else .1
        if int(self.animation_index) > self.animation_len - 1:
            self.image = self.animation[self.animation_len - 1]
            self.animation_index = 0
        else:
            self.image = self.animation[int(self.animation_index)]

    def move(self):
        global IDLE, RUN, JUMP, FALL
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.falling and not self.jumping:
            self.gravity = -15
            self.jumping = True

        if keys[pygame.K_LEFT]:
            self.rect.centerx -= 3
            self.running = True
            if not self.flip:
                IDLE = [pygame.transform.flip(x,True,False) for x in IDLE]
                RUN = [pygame.transform.flip(x,True,False) for x in RUN]
                JUMP = [pygame.transform.flip(x,True,False) for x in JUMP]
                FALL = [pygame.transform.flip(x,True,False) for x in FALL]
                self.flip = True

        elif keys[pygame.K_RIGHT]:
            self.rect.centerx += 3
            self.running = True
            if self.flip:
                IDLE = [pygame.transform.flip(x,True,False) for x in IDLE]
                RUN = [pygame.transform.flip(x,True,False) for x in RUN]
                JUMP = [pygame.transform.flip(x,True,False) for x in JUMP]
                FALL = [pygame.transform.flip(x,True,False) for x in FALL]
                self.flip = False
        else:
            self.running = False

        if self.gravity > 0 and self.rect.y < 350:
            self.falling = True

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity

    def borders(self):
        if self.rect.top <= self.floor:
            self.rect.top = self.floor
            self.gravity = 0
        if self.rect.right >= self.right_limit:
            self.rect.right = self.right_limit
        if self.rect.left <= self.left_limit:
            self.rect.left = self.left_limit
        if self.rect.bottom >= self.ground:
            self.rect.bottom = self.ground
            self.jumping = False
            self.falling = False
        if self.gravity > 15 and not self.falling:
            self.gravity = 0

    def animation_selection(self):
        if self.jumping:
            self.animation = JUMP
            self.animation_len = len(JUMP)
            if self.falling:
                self.animation = FALL
                self.animation_len = len(FALL)
        elif self.running:
            self.animation = RUN
            self.animation_len = len(RUN)
        else:
            self.animation = IDLE
            self.animation_len = len(IDLE)

    def collision(self, blocks):
        colide_up = False
        colide_down = False
        colide_right = False
        colide_left = False
        for i in blocks.sprites():
            if self.collide_rect_up.colliderect(i.collide_rect):
                self.floor = i.collide_rect.bottom
                colide_up = True
            if self.collide_rect_left.colliderect(i.collide_rect):
                self.left_limit = i.collide_rect.right
                colide_left = True
            if self.collide_rect_down.colliderect(i.collide_rect) and self.ground >= i.collide_rect.top:
                self.ground = i.collide_rect.top
                colide_down = True
            if self.collide_rect_right.colliderect(i.collide_rect) and self.right_limit >= i.collide_rect.left:
                self.right_limit = i.collide_rect.left
                colide_right = True
        if not colide_down:
            self.ground = 480
        if not colide_right:
            self.right_limit = 640
        if not colide_up:
            self.floor = 0
        if not colide_left:
            self.left_limit = 0

    def update(self, blocks):
        self.collide_rect_up = self.image.get_rect(height=100,width=10,bottom=self.rect.top, centerx=self.rect.centerx)
        self.collide_rect_down = self.image.get_rect(height=100,width=10,top=self.rect.bottom, centerx=self.rect.centerx)
        self.collide_rect_right = self.image.get_rect(centerx=self.rect.centerx, width=100,height=1,left=self.rect.right, centery=self.rect.centery)
        self.collide_rect_left = self.image.get_rect(centerx=self.rect.centerx, width=100,height=1, right=self.rect.left, centery=self.rect.centery)
        self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))

        self.apply_gravity()
        self.move()
        self.collision(blocks)
        self.borders()

        self.animate()
        self.animation_selection()

