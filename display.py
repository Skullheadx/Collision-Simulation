import random

import pygame

from box import Box
from collision import sweepAndPrune, handleParticleCollision, detectParticleCollision, spacePartitioning
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

        rows = 10
        cols = 10

        w, h = self.WIDTH / cols, self.HEIGHT / rows

        for i in range(1, 1 + cols):
            for j in range(1, 1 + rows):
                r = random.randint(10, 30)
                speed = 0.5
                self.particles.append(Particle((w * i - w / 2, h * j - h / 2),
                                               ((random.random() - 0.5) * speed, (random.random() - 0.5) * speed),
                                               (0, 0), r, r ** 2 * 3.14, self.collision_objects[0]))

        self.box = Box((0, 0), self.WIDTH, self.HEIGHT)

        self.collision_objects[0].append(self.box)

        self.collided_last_frame = set()

    def show(self):
        screen = pygame.display.set_mode(self.DIMENSIONS)
        clock = pygame.time.Clock()
        delta = 0
        self.is_running = True
        while self.is_running:
            self.update(delta)
            self.draw(screen)
            pygame.display.update()
            delta = clock.tick()
            # print(delta)
        pygame.quit()

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        self.box.update(delta)

        for particle in self.particles:
            particle.update(delta)

        for particle1, particle2 in spacePartitioning(self.particles, self.WIDTH, self.HEIGHT):
            if (particle1, particle2) not in self.collided_last_frame and (
                    particle2, particle1) not in self.collided_last_frame:
                handleParticleCollision(particle1, particle2)

                self.collided_last_frame.add((particle1, particle2))
                self.collided_last_frame.add((particle2, particle1))

            if not detectParticleCollision(particle1, particle2):
                if self.collided_last_frame.__contains__((particle1, particle2)):
                    self.collided_last_frame.remove((particle1, particle2))
                if self.collided_last_frame.__contains__((particle2, particle1)):
                    self.collided_last_frame.remove((particle2, particle1))


    def draw(self, surf):
        surf.fill(BLACK)

        self.box.draw(surf)

        for particle in self.particles:
            particle.draw(surf)

        # for p1, p2 in sweepAndPrune(self.particles):
        #     pygame.draw.line(surf, GREEN, p1.position, p2.position, 3)
