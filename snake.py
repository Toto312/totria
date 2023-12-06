import pygame

import gameobject
import image
import time_game

class Snake:
    def __init__(self, scene):
        self.scene = scene

        self.color = (240,70,61)
        self.speed = 0.28

        self.real_pos = self.scene.grid.ret_coord_grid([self.scene.limit[2]/2,self.scene.limit[3]/2])
        self.snake_body = pygame.sprite.Group()

        self.surface = image.Image([46,46])
        self.surface().fill(self.color)
        head = gameobject.GameObject(self.surface)
        head.move(self.real_pos)

        self.snake_body.add(head)
        self.head = self.snake_body.sprites()[0]
    
        # first value is time in milliseconds, the second value is the coord
        self.direction = [80, [-1,0]]
        self.last_direction = [0, [-1,0]]

        self.sprite_to_add = None
        self.collided_itself = False

    def restart(self):
        self.snake_body.empty()

        self.real_pos = self.scene.grid.ret_coord_grid([self.scene.limit[2]-30,self.scene.limit[3]-30])

        self.surface = image.Image([45,45])
        self.surface().fill(self.color)
        self.head = gameobject.GameObject(self.surface)
        self.head.change_position(self.real_pos)
        self.snake_body.add(self.head)

        # first value is time in milliseconds, the second value is the coord
        self.direction = [80, [-1,0]]
        self.last_direction = [0, [-1,0]]

    def increment_body(self):
        sprites = gameobject.GameObject(self.surface)
        pos = self.snake_body.sprites()[-1].rect[0:2]
        sprites.change_position(pos)

        self.sprite_to_add = sprites

    def change_position(self, pos):
        for i in self.snake_body.sprites():
            i.change_position(pos)

        self.real_pos = self.snake_body.sprites()[0]

    def change_direction(self, direction):
        self.last_direction = self.direction
        self.direction = [pygame.time.get_ticks(), direction]

    def is_colliding(self, rect):
        if(self.real_pos[0]+10>rect.width or self.real_pos[0]-10<0 or
           self.real_pos[1]+10>rect.height or self.real_pos[1]-10<0):
            return True
        return False

    def check_colliding_itself(self):
        for i in range(len(self.snake_body.sprites())-1):
            i+=1
            
            if(self.is_colliding(self.snake_body.sprites()[i].rect)):
                self.collided_itself = True

    def update(self):
        if(self.sprite_to_add and not pygame.sprite.spritecollideany(self.sprite_to_add,self.snake_body)):
            self.snake_body.add(self.sprite_to_add)
            self.sprite_to_add = None

        #adding an offset time when changing direction
        if((self.direction[1][0] == -self.last_direction[1][0] and self.direction[1][1] == -self.last_direction[1][1]) or
           self.direction[0]-self.last_direction[0]<120):
            self.direction = self.last_direction

        if(not self.is_colliding(self.scene.limit) and not self.collided_itself):
            self.move()
        else:
            self.scene.it_died()

    def draw(self,window,offset=[0,0]):
        for i in self.snake_body.sprites():
            #the +2 its because the snake touches the topleft since its size is 46 instead of 50 (for aesthetic purposes)
            window.blit(i.image,(i.rect[0]+offset[0]+2,i.rect[1]+offset[1]+2))

    def move(self):
        last_pos = self.head.rect[0:2]
        self.real_pos = [self.real_pos[0]+round(self.speed*self.direction[1][0]*time_game.Time().dt),self.real_pos[1]+round(self.speed*self.direction[1][1]*time_game.Time().dt)]

        self.head.change_position(self.scene.grid.ret_coord_grid(self.real_pos))
        
        if(self.head.rect[0:2]!= last_pos):
            for i in range(len(self.snake_body.sprites())-1):
                i+=1
                
                actual_pos = self.snake_body.sprites()[i].rect[0:2]
                
                #check collision (i know this doesnt make sense but is the only way it works rn)
                if(self.head.rect[0:2]==actual_pos):
                    self.collided_itself = True

                self.snake_body.sprites()[i].change_position(last_pos)
                last_pos = actual_pos[:]