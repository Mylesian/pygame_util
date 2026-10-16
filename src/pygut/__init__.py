import pygame
from pygame._sdl2 import Window
import asyncio
from base import Screen, Timer

class Application:
    '''Basic application window. Shows an optional start_screen on startup.'''
    def __init__(self, screen_size: tuple[int, int], start_screen: Screen | None = None, fps: int = 30, flags: int = 0, maximize: bool = True, vsync: int = 0, handle_init: bool = True):
        if handle_init:
            pygame.init()
        
        if maximize:
            self.showing = pygame.display.set_mode(screen_size, flags | pygame.RESIZABLE, 0, 0, vsync)
            Window.from_display_module().maximize()
        else:
            self.showing = pygame.display.set_mode(screen_size, flags, 0, 0, vsync)
        
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.screen: Screen | None = start_screen
        self.timers: list[Timer] = []
       
    def update(self, dt: float, **kwargs):
        '''Called once per frame. By default updates all of the entities in self.screen as well as count down all of its timers.
           mouse_buttons, m1_just_down, and keys_pressed are passed through kwargs. Override in a subclass to add extra functionality.'''
        if not self.screen is None:
            self.screen.update(dt=dt)
        
        for t in self.timers:
            t.countdown(dt)

    async def run(self):
        '''Runs the game loop. Framerate is set to whatever was specified on object creation. Calls pygame.quit() when the loop ends.'''
        mouse_down = False
        mouse_just_down = False
        while self.running:
            dt = 1/self.fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                if mouse_down: mouse_just_down = False
                else: mouse_just_down = True
                
                mouse_down = True
            else:
                mouse_down = False
                mouse_just_down = False
            
                 
            if not self.screen is None:
                self.screen.fill(self.screen.bgcolor)
                self.update(dt, mouse_buttons=mouse_buttons, m1_just_down=mouse_just_down, keys_pressed=pygame.key.get_pressed())
                updated = self.screen.elements.draw(self.screen)
                pygame.display.update(updated)
            
            self.clock.tick(self.fps)
            await asyncio.sleep(0)
            
        pygame.quit()
        
class WebApplication(Application):
    '''Does nothing yet. Might add more differences from Application in a future release.'''
    def __init__(self, screen_size: tuple[int, int], start_screen: Screen | None = None, fps: int = 30, flags: int = 0, vsync: int = 0, handle_init: bool = True):
        super().__init__(screen_size, start_screen, fps, flags, False, vsync, handle_init)