import pygame

import event_handler
import scene_manager
import time_game
import scenes
import image
import gameobject

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([800,800], pygame.RESIZABLE)
        self.event_handler = event_handler.EventHandler()
        self.scene_manager = scene_manager.SceneManager()
        self.time = time_game.Time()

        #im = image.Image("men.png")
        #self.sprite = gameobject.GameObject(im)
        #self.sprite.scale([600,600])
        #self.sprite.change_position([100,100])
  
        self.game_scene = scenes.GameScene()
        self.scene_manager.add_scene(self.game_scene)

    def check_game_events(self):
        if(self.event_handler.check_events("Quit")):
            pygame.quit()
            exit()

        if(key := self.event_handler.check_events("Key down")):
            # F4
            if(key.scancode == 61):
                pygame.quit()
                exit()

        if(video := self.event_handler.check_events("Video Resize")):
            width, height = video.size
            if width < 600:
                width = 600
            if height < 600:
                height = 600
            self.screen = pygame.display.set_mode((width,height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

    def mainloop(self):
        while True:
            self.time.update()

            # update events
            self.event_handler.update()
            self.check_game_events()
            self.scene_manager.update()

            # draw
            self.screen.fill((0,0,0))
            self.scene_manager.draw()
            #self.screen.blit(self.sprite.image, self.sprite.rect[0:2])
            pygame.display.flip()

if(__name__=="__main__"):
    g = Game()
    g.mainloop()