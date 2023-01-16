from colours import *
from particle import Particle
from box import Box
import pygame

pygame.init()


class Display:
    WIDTH, HEIGHT = 640, 640
    DIMENSIONS = (WIDTH, HEIGHT)
    CENTER = (WIDTH / 2, HEIGHT / 2)

    FPS = 60
    COLLISION_LAYERS = 4

    def __init__(self, window_name="Pygame"):
        self.is_running = False

        pygame.display.set_caption(window_name)

        self.collision_objects = {layer: [] for layer in range(self.COLLISION_LAYERS)}

        self.particles = [Particle(self.CENTER, (0, 0.5), (0, 0), 15, self.collision_objects[0])]
        self.collision_objects[0] += self.particles
        self.box = Box((0, 0), self.WIDTH, self.HEIGHT)
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
