import pygame

from colours import *


class Box:
    line_thickness = 5

    def __init__(self, position, width, height):
        self.position = pygame.Vector2(position)
        self.width = width
        self.height = height

        self.left = self.position.x
        self.right = self.position.x + self.width
        self.top = self.position.y
        self.bottom = self.position.y + self.height

    def update(self, delta):
        pass

    def draw(self, surf):
        pygame.draw.rect(surf, BLACK, pygame.Rect(self.left, self.top, self.width, self.height), self.line_thickness)
