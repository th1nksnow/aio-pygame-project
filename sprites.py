import pygame


class Sprites(pygame.sprite.Sprite):
    def __init__(self, x, speed, surface, score, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect(center=(x, 20))
        self.speed = speed
        self.score = score
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()
