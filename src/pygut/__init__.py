import pygame
from pygame._sdl2 import Window
import asyncio
from base import Screen, Timer

class Application:
    def __init__(self, screen_size: tuple[int, int], fps: int = 30, flags: int = 0, maximize: bool = True, vsync: int = 0, handle_init: bool = True):
        if handle_init:
            pygame.init()
            
        self.showing = pygame.display.set_mode(screen_size, flags, 0, 0, vsync)
        
        if maximize == True:
            Window.from_display_module().maximize()
        
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.screen = None
        self.timers: list[Timer] = []
       
    def update(self, dt: float):
        '''Called once per frame. By default updates all of the entities in self.screen as well as count down all of its timers.
           Override in a subclass to add extra functionality'''
        if type(self.screen) is Screen:
            self.screen.update(dt=dt)
        
        for t in self.timers:
            t.countdown(dt)

    async def run(self):
        '''Runs the game loop. Framerate is set to whatever was specified on object creation. Calls pygame.quit() when the loop ends.'''
        while self.running:
            dt = 1/self.fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            self.update(dt)
            
            pygame.display.flip()
            
            self.clock.tick(self.fps)
            await asyncio.sleep(0)
            
        pygame.quit()
        
class WebApplication(Application):
    '''Does nothing yet. Might add more differences from Application in a future release.'''
    def __init__(self, screen_size: tuple[int, int], fps: int = 30, flags: int = 0, vsync: int = 0, handle_init: bool = True):
        super().__init__(screen_size, fps, flags, False, vsync, handle_init)