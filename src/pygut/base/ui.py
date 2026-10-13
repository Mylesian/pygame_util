import pygame
from base import UIElement

class Button(UIElement):
    def __init__(self, x: float, y: float, render: pygame.Surface | str, action):
        super().__init__(x, y, render)
        self.action = action
        
    def update(self, *args, **kwargs):
        if kwargs['mouse_just_pressed'] and self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.action()