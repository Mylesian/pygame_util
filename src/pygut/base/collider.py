import pygame
from base import Collider

class RectCollider(Collider):
    def __init__(self, x: float, y: float, w: float, h: float):
        super().__init__(x, y)
        
        self.bounds = pygame.Rect(x - w/2, y - h/2, w, h)
        
    def collides(self, other: Collider):
        match other.__class__.__name__:
            case 'RectCollider':
                return self.bounds.colliderect(other.bounds) # type: ignore
        
        return False