import pygame
import sys
import random

import scene
import snake
import grid
import event_handler
import apple
import menu
import game_over
import time_game
import font

class GameScene(scene.Scene):
    def __init__(self):
        super().__init__("Game")

        self.screen = pygame.display.get_surface()
        self.last_size = pygame.display.get_window_size()
        self.event_handler = event_handler.EventHandler()
        self.grid = grid.Grid([50,50],[700,700])
        self.limit = pygame.Rect(0,0,self.screen.get_width(),self.screen.get_height())

        self.snake = snake.Snake(self)
        self.apple = apple.Apple(self)
        self.apple.relocate_position(self.snake.snake_body.sprites())

        self.menu = menu.Menu(self)
        self.game_over = game_over.GameOver()
        self.press_enter = game_over.PressEnter()
        
        self.score = 0
        self.score_font = font.Font("Resources/PixeloidSans.ttf", f"{self.score}", [self.screen.get_size()[0]*0.85,self.screen.get_size()[1]*0.1], 50)
        self.is_paused = True
        self.does_died = False

        self.increment_sound = pygame.mixer.Sound("Resources/increment.mp3")
        self.die_sound = pygame.mixer.Sound("Resources/died.mp3")
        self.died_sound_played = False

        self.music = ["Resources/music1.mp3", "Resources/music2.mp3", "Resources/music3.mp3"]
        self.now_playing = random.choice(self.music)
        pygame.mixer.music.load(random.choice(self.music))
        pygame.mixer.music.play()

    def check_events(self):
        if(button := self.event_handler.check_events("Key down")):
            if(button.key == pygame.K_p):
                self.is_paused = not self.is_paused

    def check_events_movement(self):
        if(button := self.event_handler.check_events("Key down")):
            if(button.key == pygame.K_w):
                self.snake.change_direction([0,-1])
            elif(button.key == pygame.K_s):
                self.snake.change_direction([0,1])
            elif(button.key == pygame.K_a):
                self.snake.change_direction([-1,0])
            elif(button.key == pygame.K_d):
                self.snake.change_direction([1,0])
            # enter
            elif(button.key == 13):
                if(self.does_died):
                    self.restart()
                    self.died_sound_played = False
 
    def resize(self, size):
        last_limit_position = self.limit[:]
        if size[0] == 700:
            self.limit.x = 0
        else:
            self.limit.x = (size[0] - self.last_size[0]) / 2
        if size[1] == 700:
            self.limit.y = 0
        else:
            self.limit.y = (size[1] - self.last_size[0]) / 2

        self.game_over = game_over.GameOver()
        self.press_enter = game_over.PressEnter()
        self.menu.resize()

    def restart(self):
        self.score = 0
        self.does_died = False
        self.press_enter.is_active = False
        self.snake = snake.Snake(self)
        self.apple.relocate_position(self.snake.snake_body.sprites())

    def check_collision(self):
        if(self.apple.rect.collidepoint(self.snake.head.rect[0:2])):
            self.snake.increment_body()
            self.apple.relocate_position(self.snake.snake_body.sprites())
            self.score += 1
            self.increment_sound.play()


    def it_died(self):
        if(not self.died_sound_played):
            self.die_sound.play()
            self.died_sound_played = True
        self.press_enter.restart()
        self.game_over.restart()
        self.does_died = True

    def update(self):
        if(not pygame.mixer.music.get_busy()):
            next = (self.music.index(self.now_playing)+1)//(len(self.music)-1)
            print(next)
            self.now_playing = self.music[next]
            pygame.mixer.music.load(self.now_playing)
            pygame.mixer.music.play()

        self.score_font.change_text(f"{self.score}")
        self.score_font.change_position([self.screen.get_size()[0]*0.9,self.screen.get_size()[1]*0.1])

        if(self.does_died):
            self.game_over.update(time_game.Time().dt)
            self.press_enter.is_active = True

        self.check_events()

        if(not self.is_paused):
            self.check_events_movement()
            self.snake.update()
            self.check_collision()
            self.press_enter.update(time_game.Time().dt)
        else: 
            self.menu.update()

    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        pygame.draw.rect(self.screen,(45,45,45),self.limit,4,2)

        self.snake.draw(self.screen,self.limit)
        self.screen.blit(self.apple.image,(self.apple.rect[0]+self.limit.x,self.apple.rect[1]+self.limit.y))

        if(self.does_died):
            self.game_over.draw(self.screen)
            self.press_enter.draw(self.screen)
    
        if(self.is_paused):
            self.menu.draw(self.screen)

        self.score_font.draw(self.screen)

class MenuScene(scene.Scene):
    def __init__(self):
        super().__init__("Menu")

        self.screen = pygame.display.get_surface()
        self.event_handler = event_handler.EventHandler()
        