import pygame
import random

from box import Box
from colours import *
from particle import Particle

pygame.init()


class Display:
    WIDTH, HEIGHT = 1080, 720
    DIMENSIONS = (WIDTH, HEIGHT)
    CENTER = (WIDTH / 2, HEIGHT / 2)

    FPS = 0
    COLLISION_LAYERS = 4

    def __init__(self, window_name="Pygame"):
        self.is_running = False

        pygame.display.set_caption(window_name)

        self.collision_objects = {layer: [] for layer in range(self.COLLISION_LAYERS)}
        self.particles = []

        n = 5
        for i in range(1, n):
            for j in range(1, n):
                m = random.randint(35, 45)
                speed = 0.1
                self.particles.append(Particle((self.WIDTH / n * i, self.HEIGHT / n * j),
                                               ((random.random() - 0.5) * speed, (random.random() - 0.5) * speed),
                                               (0, 0), m, 100, self.collision_objects[0]))

        self.box = Box((0, 0), self.WIDTH, self.HEIGHT)

        self.collision_objects[0] += self.particles
        self.collision_objects[0].append(self.box)

    def show(self):
        screen = pygame.display.set_mode(self.DIMENSIONS)
        clock = pygame.time.Clock()
        delta = 0
        self.is_running = True
        while self.is_running:
            self.update(delta)
            self.draw(screen)
            pygame.display.flip()
            delta = clock.tick(self.FPS)
            print(delta)
        pygame.quit()

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        self.box.update(delta)

        for particle in self.particles:
            particle.update(delta)

    def draw(self, surf):
        surf.fill(WHITE)

        self.box.draw(surf)

        for particle in self.particles:
            particle.draw(surf)
