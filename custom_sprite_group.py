import pygame

class CustomSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)
            
    def reset(self):
        for sprite in self.sprites():
            sprite.reset()